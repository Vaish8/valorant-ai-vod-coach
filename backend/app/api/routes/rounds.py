from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.round import RoundCreate, RoundResponse
from app.services.round_service import create_round, get_rounds_for_match

router = APIRouter(tags=["Rounds"])


@router.post(
    "/matches/{match_id}/rounds",
    response_model=RoundResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_match_round(
    match_id: int,
    round_data: RoundCreate,
    db: Session = Depends(get_db),
):
    round_obj = create_round(db=db, match_id=match_id, round_data=round_data)

    if round_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return round_obj


@router.get(
    "/matches/{match_id}/rounds",
    response_model=list[RoundResponse],
)
def list_match_rounds(
    match_id: int,
    db: Session = Depends(get_db),
):
    rounds = get_rounds_for_match(db=db, match_id=match_id)

    if rounds is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    return rounds