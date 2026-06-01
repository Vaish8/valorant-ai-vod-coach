from enum import Enum


class RoundSide(str, Enum):
    attack = "attack"
    defense = "defense"


class RoundResult(str, Enum):
    won = "won"
    lost = "lost"


class EventType(str, Enum):
    first_death = "first_death"
    trade_kill = "trade_kill"
    utility_unused = "utility_unused"
    spike_planted = "spike_planted"
    spike_defused = "spike_defused"
    post_plant_loss = "post_plant_loss"
    overpeek = "overpeek"
    isolated_duel = "isolated_duel"
    late_rotation = "late_rotation"