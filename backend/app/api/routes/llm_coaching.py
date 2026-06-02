from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.llm_coaching import LLMCoachingResponse
from app.services.llm_coaching_service import generate_llm_coaching_text

router = APIRouter(tags=["LLM Coaching"])


@router.post(
    "/matches/{match_id}/llm-coaching",
    response_model=LLMCoachingResponse,
)
def create_llm_coaching_response(
    match_id: int,
    db: Session = Depends(get_db),
):
    coaching_response = generate_llm_coaching_text(db=db, match_id=match_id)

    if coaching_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return coaching_response