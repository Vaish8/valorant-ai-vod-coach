from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.coach_summary import CoachSummaryResponse
from app.services.coach_summary_service import (
    generate_and_save_coach_summary,
    get_coach_summary,
)

router = APIRouter(tags=["Coach Summary"])


@router.post(
    "/matches/{match_id}/coach-summary",
    response_model=CoachSummaryResponse,
)
def create_match_coach_summary(
    match_id: int,
    db: Session = Depends(get_db),
):
    summary = generate_and_save_coach_summary(db=db, match_id=match_id)

    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return summary


@router.get(
    "/matches/{match_id}/coach-summary",
    response_model=CoachSummaryResponse,
)
def get_match_coach_summary(
    match_id: int,
    db: Session = Depends(get_db),
):
    summary = get_coach_summary(db=db, match_id=match_id)

    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coach summary for match with id {match_id} not found",
        )

    return summary