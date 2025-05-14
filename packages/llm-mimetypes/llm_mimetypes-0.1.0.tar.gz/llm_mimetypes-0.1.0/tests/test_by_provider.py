import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize("provider_name,expected_model", [
    ("openai", "gpt-4"),
    ("anthropic", "claude-3-opus"),
    ("google", "gemini-pro"),
])
async def test_get_models_by_provider(provider_name: str, expected_model: str):
    from llm_mimetypes.by_provider import get_models_by_provider

    models = await get_models_by_provider(provider_name)

    assert isinstance(models, list)
    assert expected_model in models
