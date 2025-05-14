import sqlite3

def initialize_database(db_path='models.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    -- Models table
    CREATE TABLE IF NOT EXISTS models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        context_length INTEGER NOT NULL
    );

    -- Mime types table
    CREATE TABLE IF NOT EXISTS mime_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        media_type TEXT NOT NULL UNIQUE  -- e.g. 'text/plain', 'application/json'
    );

    -- Providers table
    CREATE TABLE IF NOT EXISTS providers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL
    );

    -- API types table (for OpenAI, Anthropic etc)
    CREATE TABLE IF NOT EXISTS api_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE  -- e.g. 'openai', 'anthropic'
    );

    -- Model input mime types (many-to-many)
    CREATE TABLE IF NOT EXISTS model_input_mime_types (
        model_id INTEGER NOT NULL,
        mime_type_id INTEGER NOT NULL,
        PRIMARY KEY (model_id, mime_type_id),
        FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE CASCADE,
        FOREIGN KEY (mime_type_id) REFERENCES mime_types(id) ON DELETE CASCADE
    );

    -- Model output mime types (many-to-many)
    CREATE TABLE IF NOT EXISTS model_output_mime_types (
        model_id INTEGER NOT NULL,
        mime_type_id INTEGER NOT NULL,
        PRIMARY KEY (model_id, mime_type_id),
        FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE CASCADE,
        FOREIGN KEY (mime_type_id) REFERENCES mime_types(id) ON DELETE CASCADE
    );

    -- Model to provider + API type mapping
    CREATE TABLE IF NOT EXISTS model_provider_api (
        model_id INTEGER NOT NULL,
        provider_id INTEGER NOT NULL,
        api_type_id INTEGER NOT NULL,
        PRIMARY KEY (model_id, provider_id, api_type_id),
        FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE CASCADE,
        FOREIGN KEY (provider_id) REFERENCES providers(id) ON DELETE CASCADE,
        FOREIGN KEY (api_type_id) REFERENCES api_types(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
