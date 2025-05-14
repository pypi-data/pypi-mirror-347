import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize("mime_type", ["text/plain", "text/markdown", "text/html"])
async def test_get_models_by_input_mime_type_text(mime_type: str):
    from llm_mimetypes.by_mime_type import get_models_by_input_mime_type

    models = await get_models_by_input_mime_type(mime_type)

    assert isinstance(models, list)
    assert len(models) > 0
    assert "gpt-4" in models
    assert "claude-3-opus" in models
    assert "gemini-pro" in models


@pytest.mark.asyncio
@pytest.mark.parametrize("mime_type", ["image/png", "image/jpeg", "image/gif"])
async def test_get_models_by_input_mime_type_image(mime_type: str):
    from llm_mimetypes.by_mime_type import get_models_by_input_mime_type

    models = await get_models_by_input_mime_type(mime_type)

    assert isinstance(models, list)
    assert len(models) > 0
    assert "gemini-pro" in models


@pytest.mark.asyncio
@pytest.mark.parametrize("mime_type", ["text/plain"])
async def test_get_models_by_output_mime_type(mime_type: str):
    from llm_mimetypes.by_mime_type import get_models_by_output_mime_type

    models = await get_models_by_output_mime_type(mime_type)

    assert isinstance(models, list)
    assert len(models) > 0
    assert "gpt-4" in models


@pytest.mark.asyncio
@pytest.mark.parametrize("mime_type", ["application/x-unknown", "none", "text/this-is-not-a-mime-type", "", "a"*64])
async def test_get_models_by_unknown_mime_type(mime_type: str):
    from llm_mimetypes.by_mime_type import get_models_by_input_mime_type, get_models_by_output_mime_type

    for fn in (get_models_by_input_mime_type, get_models_by_output_mime_type):
        models = await fn(mime_type)
        assert isinstance(models, list)
        assert models == []