import sqlite3

def insert_providers(db_path='models.db'):
    providers = [
        ("openai", "https://openai.com/"),
        ("google", "https://cloud.google.com/"),
        ("anthropic", "https://www.anthropic.com/"),
        ("ai21", "https://www.ai21.com/"),
        ("deepinfra", "https://deepinfra.com/"),
        ("together", "https://www.together.ai/"),
        ("alibaba", "https://damo.alibaba.com/"),
        ("amazon bedrock", "https://aws.amazon.com/bedrock/"),
        ("cohere", "https://cohere.ai/"),
        ("deepseek", "https://www.deepseek.com/"),
        ("avian", "https://avian.ai/"),
        ("groq", "https://groq.com/"),
        ("cloudflare", "https://www.cloudflare.com/"),
        ("glama", "https://glama.ai/"),
        ("google ai studio", "https://makersuite.google.com/"),
        ("mistral", "https://www.mistral.ai/"),
        ("fireworks", "https://fireworks.ai/"),
        ("azure", "https://azure.microsoft.com/"),
        ("perplexity", "https://www.perplexity.ai/"),
        ("xai", "https://x.ai/"),
    ]


    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT OR IGNORE INTO providers (name, url)
    VALUES (?, ?)
    """, providers)

    conn.commit()
    conn.close()
