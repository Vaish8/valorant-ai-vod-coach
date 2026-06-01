from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.event import Event
from app.db.models.round import Round
from app.schemas.event import EventCreate


def create_event(db: Session, round_id: int, event_data: EventCreate) -> Event | None:
    round_obj = db.get(Round, round_id)

    if round_obj is None:
        return None

    event = Event(
        round_id=round_id,
        timestamp_seconds=event_data.timestamp_seconds,
        event_type=event_data.event_type.value,
        actor=event_data.actor,
        target=event_data.target,
        location=event_data.location,
        description=event_data.description,
        source=event_data.source,
        confidence=event_data.confidence,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def get_events_for_round(db: Session, round_id: int) -> Sequence[Event] | None:
    round_obj = db.get(Round, round_id)

    if round_obj is None:
        return None

    statement = (
        select(Event)
        .where(Event.round_id == round_id)
        .order_by(Event.timestamp_seconds.asc())
    )

    return db.scalars(statement).all()