from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import create_event, get_events_for_round

router = APIRouter(tags=["Events"])


@router.post(
    "/rounds/{round_id}/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_round_event(
    round_id: int,
    event_data: EventCreate,
    db: Session = Depends(get_db),
):
    event = create_event(db=db, round_id=round_id, event_data=event_data)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Round with id {round_id} not found",
        )

    return event


@router.get(
    "/rounds/{round_id}/events",
    response_model=list[EventResponse],
)
def list_round_events(
    round_id: int,
    db: Session = Depends(get_db),
):
    events = get_events_for_round(db=db, round_id=round_id)

    if events is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Round with id {round_id} not found",
        )

    return events