from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.statistics import MatchStatisticsResponse
from app.services.statistics_service import calculate_match_statistics

router = APIRouter(tags=["Statistics"])


@router.get(
    "/matches/{match_id}/statistics",
    response_model=MatchStatisticsResponse,
)
def get_match_statistics(
    match_id: int,
    db: Session = Depends(get_db),
):
    statistics = calculate_match_statistics(db=db, match_id=match_id)

    if statistics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return statistics