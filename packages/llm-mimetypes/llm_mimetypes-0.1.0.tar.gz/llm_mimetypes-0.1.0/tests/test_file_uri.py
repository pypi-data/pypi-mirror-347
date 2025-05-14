import aiosqlite
import pytest

def test_file_uri():
    from llm_mimetypes.file import get_db_uri

    db_uri = get_db_uri()
    assert db_uri.startswith("file:")
    assert "?mode=ro" in db_uri
    assert "models.db" in db_uri


@pytest.mark.asyncio
async def test_open_db():
    from llm_mimetypes.file import get_db_uri

    db_uri = get_db_uri()
    print(f"DB URI: {db_uri}")
    async with aiosqlite.connect(db_uri, uri=True) as db:
        assert db is not None
        cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = await cursor.fetchall()
        assert len(tables) > 0, "No tables found in the database." # type: ignore