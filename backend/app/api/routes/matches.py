from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.match import MatchCreate, MatchResponse
from app.services.match_service import create_match, get_match_by_id, get_matches

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post(
    "",
    response_model=MatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_match_session(
    match_data: MatchCreate,
    db: Session = Depends(get_db),
):
    return create_match(db=db, match_data=match_data)


@router.get("", response_model=list[MatchResponse])
def list_match_sessions(db: Session = Depends(get_db)):
    return get_matches(db=db)


@router.get("/{match_id}", response_model=MatchResponse)
def get_match_session(
    match_id: int,
    db: Session = Depends(get_db),
):
    match = get_match_by_id(db=db, match_id=match_id)

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return match