from mime_types_list import mime_types
import sqlite3

def insert_mime_types(db_path='models.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    mt = [(m,) for m in mime_types]

    cursor.executemany("""
    INSERT INTO mime_types (media_type)
    VALUES (?)
    """, mt)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_mime_types()
