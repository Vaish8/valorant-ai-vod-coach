from pydantic import BaseModel


class LLMCoachingResponse(BaseModel):
    match_id: int
    provider: str
    model: str
    prompt_type: str
    generated_text: str