from llm_mimetypes.file import get_db_uri
import aiosqlite

async def get_models_by_provider(provider_name: str) -> list[str]:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT DISTINCT models.name
            FROM providers
            JOIN model_provider_api ON providers.id = model_provider_api.provider_id
            JOIN models ON models.id = model_provider_api.model_id
            WHERE providers.name = ?
        """, (provider_name,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
