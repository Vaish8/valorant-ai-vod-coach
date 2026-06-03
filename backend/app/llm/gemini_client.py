from google import genai

from app.core.config import settings
from app.llm.base import LLMClient


class GeminiClient(LLMClient):
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required when LLM_PROVIDER is set to 'gemini'."
            )

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.LLM_MODEL

    def generate_text(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if response.text is None:
            return "No coaching response was generated."

        return response.text