from llm_mimetypes.file import get_db_uri
import aiosqlite


async def get_input_mime_types_by_model(model_name: str) -> list[str]:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT mime_types.media_type
            FROM models
            JOIN model_input_mime_types ON models.id = model_input_mime_types.model_id
            JOIN mime_types ON mime_types.id = model_input_mime_types.mime_type_id
            JOIN model_provider_api ON models.id = model_provider_api.model_id
            JOIN providers ON model_provider_api.provider_id = providers.id
            JOIN api_types ON model_provider_api.api_type_id = api_types.id
            WHERE models.name = ?;
        """, (model_name,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_output_mime_types_by_model(model_name: str) -> list[str]:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT mime_types.media_type
            FROM models
            JOIN model_output_mime_types ON models.id = model_output_mime_types.model_id
            JOIN mime_types ON mime_types.id = model_output_mime_types.mime_type_id
            WHERE models.name = ?
        """, (model_name,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_context_length_by_model(model_name: str) -> int | None:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT context_length
            FROM models
            WHERE name = ?
        """, (model_name,))
        row = await cursor.fetchone()
        return row[0] if row else None


async def get_providers_by_model(model_name: str) -> list[tuple[str, str]]:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT providers.name, providers.url
            FROM models
            JOIN model_provider_api ON models.id = model_provider_api.model_id
            JOIN providers ON model_provider_api.provider_id = providers.id
            WHERE models.name = ?
        """, (model_name,))
        return await cursor.fetchall()


async def get_api_types_by_model(model_name: str) -> list[str]:
    db_uri = get_db_uri()
    async with aiosqlite.connect(db_uri, uri=True) as db:
        cursor = await db.execute("""
            SELECT DISTINCT api_types.name
            FROM models
            JOIN model_provider_api ON models.id = model_provider_api.model_id
            JOIN api_types ON model_provider_api.api_type_id = api_types.id
            WHERE models.name = ?
        """, (model_name,))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_full_model_metadata(model_name: str) -> dict:
    context = await get_context_length_by_model(model_name)
    input_mime = await get_input_mime_types_by_model(model_name)
    output_mime = await get_output_mime_types_by_model(model_name)
    providers = await get_providers_by_model(model_name)
    api_types = await get_api_types_by_model(model_name)
    
    return {
        "name": model_name,
        "context_length": context,
        "input_mime_types": input_mime,
        "output_mime_types": output_mime,
        "providers": [{"name": name, "url": url} for name, url in providers],
        "api_types": api_types
    }
