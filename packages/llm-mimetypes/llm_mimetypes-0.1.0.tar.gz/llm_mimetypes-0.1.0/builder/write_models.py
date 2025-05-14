import sqlite3

def insert_models_with_provider_and_api(db_path='models.db'):
    # (model_name, context_length, provider_name, api_type_name)
    model_entries = [
        ("gpt-4", 128000, "openai", "openai-like"),
        ("gemini-pro", 32000, "google", "vertex"),
        ("claude-3-opus", 200000, "anthropic", "anthropic"),

        ("gpt-4.1", 128000, "openai", "openai-like"),
        ("gpt-4o", 128000, "openai", "openai-like"),
        ("gpt-4.5", 128000, "openai", "openai-like"),
        ("gpt-4o-mini", 128000, "openai", "openai-like"),
        ("o3", 200000, "openai", "openai-like"),
        ("o4-mini", 200000, "openai", "openai-like"),

        ("claude-3-5-haiku", 200000, "anthropic", "anthropic"),
        ("claude-3-5-sonnet", 200000, "anthropic", "anthropic"),
        ("claude-3-7-sonnet", 200000, "anthropic", "anthropic"),

        ("gemini-1.5-pro", 1000000, "google", "vertex"),
        ("gemini-1.5-flash", 1000000, "google", "vertex"),
        ("gemini-2.0-pro", 1000000, "google", "vertex"),
        ("gemini-2.0-flash", 1000000, "google", "vertex"),
        ("gemini-2.5-pro", 1000000, "google", "vertex"),
        ("gemini-2.5-flash", 1000000, "google", "vertex"),

        ("command-r-plus", 128000, "cohere", "custom"),
        ("command-r", 128000, "cohere", "custom"),

        ("llama-3.1-70b-instruct", 128000, "avian", "custom"),
        ("llama-3.1-8b-instruct", 128000, "avian", "custom"),
        ("llama-3.2-11b-vision-instruct", 128000, "together", "custom"),
        ("llama-3-70b-instruct", 8000, "deepinfra", "custom"),
        ("llama-3-8b-instruct", 8000, "deepinfra", "custom"),

        ("jamba-1-5-large", 256000, "ai21", "custom"),
        ("jamba-instruct", 256000, "ai21", "custom"),

        ("qwen-2.5-72b-instruct", 131072, "deepinfra", "custom"),
        ("qwen-2.5-7b-instruct", 131072, "together", "custom"),
        ("qwen-plus", 131072, "alibaba", "custom"),
        ("qwen-turbo", 1000000, "alibaba", "custom"),

        ("phi-3.5-mini-128k-instruct", 128000, "azure", "custom"),
        ("phi-3-medium-128k-instruct", 128000, "azure", "custom"),

        ("grok-3", 131072, "xai", "custom"),
        ("grok-3-fast-beta", 131072, "xai", "custom"),
        ("grok-3-mini-beta", 131072, "xai", "custom"),
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Build lookup maps once
    cursor.execute("SELECT id, name FROM providers")
    provider_map = {name: id for id, name in cursor.fetchall()}

    cursor.execute("SELECT id, name FROM api_types")
    api_type_map = {name: id for id, name in cursor.fetchall()}

    cursor.execute("SELECT id, name FROM models")
    model_map = {name: id for id, name in cursor.fetchall()}

    for model_name, context_length, provider_name, api_type_name in model_entries:
        # Insert model if not present
        model_id = model_map.get(model_name)
        if not model_id:
            cursor.execute("""
            INSERT INTO models (name, context_length)
            VALUES (?, ?)
            """, (model_name, context_length))
            model_id = cursor.lastrowid
            model_map[model_name] = model_id

        # Resolve provider ID
        provider_id = provider_map.get(provider_name)
        if provider_id is None:
            raise ValueError(f"Unknown provider: {provider_name}")

        # Resolve API type ID
        api_type_id = api_type_map.get(api_type_name)
        if api_type_id is None:
            raise ValueError(f"Unknown API type: {api_type_name}")

        # Insert into model_provider_api
        cursor.execute("""
        INSERT OR IGNORE INTO model_provider_api (model_id, provider_id, api_type_id)
        VALUES (?, ?, ?)
        """, (model_id, provider_id, api_type_id))

    conn.commit()
    conn.close()
