from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analysis import PersistedMatchAnalysisResponse
from app.services.analysis_service import (
    get_saved_analysis_findings,
    run_and_save_analysis,
)

router = APIRouter(tags=["Analysis"])


@router.post(
    "/matches/{match_id}/analyze",
    response_model=PersistedMatchAnalysisResponse,
)
def analyze_match_endpoint(
    match_id: int,
    db: Session = Depends(get_db),
):
    analysis = run_and_save_analysis(db=db, match_id=match_id)

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return analysis


@router.get(
    "/matches/{match_id}/analysis",
    response_model=PersistedMatchAnalysisResponse,
)
def get_match_analysis(
    match_id: int,
    db: Session = Depends(get_db),
):
    analysis = get_saved_analysis_findings(db=db, match_id=match_id)

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return analysis