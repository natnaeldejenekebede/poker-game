# src/poker_game/models/hand.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Dict, List

@dataclass
class Hand:
    id: UUID
    stacks: Dict[str, int]  # e.g., {"P1": 1125600, "P2": 1125600, ...}
    dealer_position: int
    small_blind_position: int
    big_blind_position: int
    player_cards: Dict[str, List[str]]  # e.g., {"P1": ["Ac", "Ad"], ...}
    action_sequence: str  # e.g., "fff:c:b40:5c6c7c"
    winnings: Dict[str, int]  # e.g., {"P1": -40, "P2": 80, ...}
    created_at: datetime