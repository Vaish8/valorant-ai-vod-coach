from pydantic import BaseModel


class CoachPromptResponse(BaseModel):
    match_id: int
    prompt_type: str
    prompt: str