from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.match import Match
from app.schemas.match import MatchCreate


def create_match(db: Session, match_data: MatchCreate) -> Match:
    match = Match(
        title=match_data.title,
        map_name=match_data.map_name,
        player_agent=match_data.player_agent,
        rank=match_data.rank,
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def get_matches(db: Session) -> Sequence[Match]:
    statement = select(Match).order_by(Match.created_at.desc())
    return db.scalars(statement).all()


def get_match_by_id(db: Session, match_id: int) -> Match | None:
    statement = select(Match).where(Match.id == match_id)
    return db.scalars(statement).first()