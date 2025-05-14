import sqlite3
import re

model_mime_map = {
    "gpt-4": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain"]
    },
    "gpt-4o": {
        "input": ["text/*", "application/json", "image/*", "audio/*"],
        "output": ["text/plain", "application/json"]
    },
    "gpt-4.5": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain"]
    },
    "gpt-4o-mini": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain"]
    },
    "gemini-pro": {
        "input": ["text/*", "application/json", "image/*"],
        "output": ["text/plain"]
    },
    "gemini-1.5-pro": {
        "input": ["text/*", "application/json", "image/*", "audio/*"],
        "output": ["text/plain", "application/json"]
    },
    "gemini-1.5-flash": {
        "input": ["text/*", "application/json", "image/*"],
        "output": ["text/plain"]
    },
    "gemini-2.0-pro": {
        "input": ["text/*", "application/json", "image/*"],
        "output": ["text/plain", "application/json"]
    },
    "gemini-2.0-flash": {
        "input": ["text/*", "application/json", "image/*"],
        "output": ["text/plain"]
    },
    "claude-3-opus": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain"]
    },
    "claude-3-5-haiku": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain"]
    },
    "claude-3-5-sonnet": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain"]
    },
    "claude-3-7-sonnet": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain"]
    },
    "command-r-plus": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain", "application/json"]
    },
    "command-r": {
        "input": ["text/*"],
        "output": ["text/plain"]
    },
    "llama-3.1-70b-instruct": {
        "input": ["text/*"],
        "output": ["text/plain"]
    },
    "llama-3.2-11b-vision-instruct": {
        "input": ["text/*", "image/*"],
        "output": ["text/plain"]
    },
    "jamba-instruct": {
        "input": ["text/*"],
        "output": ["text/plain"]
    },
    "qwen-2.5-72b-instruct": {
        "input": ["text/*"],
        "output": ["text/plain"]
    },
    "qwen-turbo": {
        "input": ["text/*", "application/json"],
        "output": ["text/plain", "application/json"]
    },
    "phi-3.5-mini-128k-instruct": {
        "input": ["text/*"],
        "output": ["text/plain"]
    },
    "grok-3": {
        "input": ["text/*", "application/json", "image/*"],
        "output": ["text/plain"]
    }
}

def associate_model_mime_types_patterned(db_path='models.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM models")
    model_map = {name: id for id, name in cursor.fetchall()}

    cursor.execute("SELECT id, media_type FROM mime_types")
    mime_list = cursor.fetchall()

    for model_name, mime_config in model_mime_map.items():
        model_id = model_map.get(model_name)
        if model_id is None:
            raise ValueError(f"Unknown model: {model_name}")

        for mode, patterns in mime_config.items():
            for pattern in patterns:
                regex = re.compile("^" + re.escape(pattern).replace(r"\*", ".*") + "$")

                matching_mimes = [mime_id for mime_id, media_type in mime_list if regex.match(media_type)]

                for mime_id in matching_mimes:
                    table = (
                        "model_input_mime_types" if mode == "input"
                        else "model_output_mime_types"
                    )
                    cursor.execute(f"""
                    INSERT OR IGNORE INTO {table} (model_id, mime_type_id)
                    VALUES (?, ?)
                    """, (model_id, mime_id))

    conn.commit()
    conn.close()
