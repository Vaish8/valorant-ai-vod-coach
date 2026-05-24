from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.match import Match
from app.db.models.round import Round
from app.schemas.round import RoundCreate


def create_round(db: Session, match_id: int, round_data: RoundCreate) -> Round | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    round_obj = Round(
        match_id=match_id,
        round_number=round_data.round_number,
        side=round_data.side,
        round_result=round_data.round_result,
        spike_planted=round_data.spike_planted,
        site=round_data.site,
        start_time_seconds=round_data.start_time_seconds,
        end_time_seconds=round_data.end_time_seconds,
    )

    db.add(round_obj)
    db.commit()
    db.refresh(round_obj)

    return round_obj


def get_rounds_for_match(db: Session, match_id: int) -> Sequence[Round] | None:
    match = db.get(Match, match_id)

    if match is None:
        return None

    statement = (
        select(Round)
        .where(Round.match_id == match_id)
        .order_by(Round.round_number.asc())
    )

    return db.scalars(statement).all()


def get_round_by_id(db: Session, round_id: int) -> Round | None:
    return db.get(Round, round_id)