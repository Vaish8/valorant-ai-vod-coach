from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analysis import MatchAnalysisResponse
from app.services.rule_engine import analyze_match

router = APIRouter(tags=["Analysis"])


@router.post(
    "/matches/{match_id}/analyze",
    response_model=MatchAnalysisResponse,
)
def analyze_match_endpoint(
    match_id: int,
    db: Session = Depends(get_db),
):
    analysis = analyze_match(db=db, match_id=match_id)

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return analysis