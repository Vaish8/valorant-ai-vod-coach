from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.coach_prompt import CoachPromptResponse
from app.services.coach_prompt_builder import build_coach_prompt

router = APIRouter(tags=["Coach Prompt"])


@router.get(
    "/matches/{match_id}/coach-prompt",
    response_model=CoachPromptResponse,
)
def get_match_coach_prompt(
    match_id: int,
    db: Session = Depends(get_db),
):
    prompt = build_coach_prompt(db=db, match_id=match_id)

    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return prompt