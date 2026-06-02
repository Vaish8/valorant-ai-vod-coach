from app.core.config import settings
from app.llm.base import LLMClient
from app.llm.mock_client import MockLLMClient


def get_llm_client() -> LLMClient:
    if settings.LLM_PROVIDER == "mock":
        return MockLLMClient()

    raise ValueError(
        f"Unsupported LLM_PROVIDER '{settings.LLM_PROVIDER}'. "
        "Currently supported providers: mock"
    )