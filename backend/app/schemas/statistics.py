from typing import Dict

from pydantic import BaseModel


class MatchStatisticsResponse(BaseModel):
    match_id: int

    total_rounds: int
    rounds_won: int
    rounds_lost: int

    attack_rounds: int
    defense_rounds: int
    attack_rounds_won: int
    defense_rounds_won: int

    attack_win_rate: float
    defense_win_rate: float
    overall_win_rate: float

    spike_plants: int
    post_plant_losses: int

    total_events: int
    event_counts_by_type: Dict[str, int]

    first_death_count: int
    utility_unused_count: int
    trade_kill_count: int