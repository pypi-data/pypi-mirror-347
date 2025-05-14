import pytest

MODELS = ["gpt-4", "claude-3-opus", "gemini-pro"]

@pytest.mark.asyncio
@pytest.mark.parametrize("model", MODELS)
async def test_get_input_mime_types_by_model(model: str):
    from llm_mimetypes.by_model import get_input_mime_types_by_model

    mime_types = await get_input_mime_types_by_model(model)
    
    assert isinstance(mime_types, list)
    assert len(mime_types) > 0
    assert "text/plain" in mime_types
    assert "text/markdown" in mime_types
    assert "text/html" in mime_types


@pytest.mark.asyncio
@pytest.mark.parametrize("model", MODELS)
async def test_get_output_mime_types_by_model(model: str):
    from llm_mimetypes.by_model import get_output_mime_types_by_model

    mime_types = await get_output_mime_types_by_model(model)
    
    assert isinstance(mime_types, list)
    assert len(mime_types) > 0
    assert "text/plain" in mime_types


@pytest.mark.asyncio
@pytest.mark.parametrize("model", MODELS)
async def test_get_context_length_by_model(model: str):
    from llm_mimetypes.by_model import get_context_length_by_model

    ctx = await get_context_length_by_model(model)
    
    assert isinstance(ctx, int)
    assert ctx > 0


@pytest.mark.asyncio
@pytest.mark.parametrize("model", MODELS)
async def test_get_providers_by_model(model: str):
    from llm_mimetypes.by_model import get_providers_by_model

    providers = await get_providers_by_model(model)
    
    assert isinstance(providers, list)
    assert all(isinstance(p, tuple) and len(p) == 2 for p in providers)
    assert all(p[0] for p in providers)


@pytest.mark.asyncio
@pytest.mark.parametrize("model", MODELS)
async def test_get_api_types_by_model(model: str):
    from llm_mimetypes.by_model import get_api_types_by_model

    api_types = await get_api_types_by_model(model)

    assert isinstance(api_types, list)
    assert len(api_types) > 0
    assert all(isinstance(api, str) for api in api_types)


@pytest.mark.asyncio
@pytest.mark.parametrize("model", MODELS)
async def test_get_full_model_metadata(model: str):
    from llm_mimetypes.by_model import get_full_model_metadata

    metadata = await get_full_model_metadata(model)

    assert isinstance(metadata, dict)
    assert metadata["name"] == model
    assert isinstance(metadata["context_length"], int) and metadata["context_length"] > 0
    assert isinstance(metadata["input_mime_types"], list) and len(metadata["input_mime_types"]) > 0
    assert isinstance(metadata["output_mime_types"], list) and len(metadata["output_mime_types"]) > 0
    assert isinstance(metadata["providers"], list) and len(metadata["providers"]) > 0
    assert isinstance(metadata["api_types"], list) and len(metadata["api_types"]) > 0
