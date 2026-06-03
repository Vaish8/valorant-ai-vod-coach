from sqlalchemy.orm import Session

from app.core.config import settings
from app.llm.factory import get_llm_client
from app.services.coach_prompt_builder import build_coach_prompt


def generate_llm_coaching_text(
    db: Session,
    match_id: int,
) -> dict | None:
    prompt_response = build_coach_prompt(db=db, match_id=match_id)

    if prompt_response is None:
        return None

    prompt = prompt_response["prompt"]
    llm_client = get_llm_client()
    generated_text = llm_client.generate_text(prompt=prompt)

    return {
        "match_id": match_id,
        "provider": settings.LLM_PROVIDER,
        "model": settings.LLM_MODEL,
        "prompt_type": prompt_response["prompt_type"],
        "generated_text": generated_text,
    }