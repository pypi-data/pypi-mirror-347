import sqlite3

def insert_api_types(db_path='models.db'):
    api_types = [
        ("openai-like",),
        ("vertex",),
        ("anthropic",),
        ("custom",)
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT OR IGNORE INTO api_types (name)
    VALUES (?)
    """, api_types)

    conn.commit()
    conn.close()
