from llm_mimetypes.file import get_db_uri
import aiosqlite

async def get_models_by_input_mime_type(media_type: str) -> list[str]:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT models.name
            FROM mime_types
            JOIN model_input_mime_types ON mime_types.id = model_input_mime_types.mime_type_id
            JOIN models ON models.id = model_input_mime_types.model_id
            WHERE mime_types.media_type = ?
        """, (media_type,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_models_by_output_mime_type(media_type: str) -> list[str]:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT models.name
            FROM mime_types
            JOIN model_output_mime_types ON mime_types.id = model_output_mime_types.mime_type_id
            JOIN models ON models.id = model_output_mime_types.model_id
            WHERE mime_types.media_type = ?
        """, (media_type,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
