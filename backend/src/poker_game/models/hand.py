# src/poker_game/models/hand.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    
    def __post_init__(self):
        # Log the initial state of winnings
        logger.debug(f"Hand.__post_init__ called with winnings: {self.winnings}")
        
        # Validate winnings dictionary
        expected_players = {f"P{i+1}" for i in range(6)}
        if not isinstance(self.winnings, dict):
            logger.error(f"Invalid winnings type: {type(self.winnings)}, expected dict")
            raise ValueError("Winnings must be a dictionary")
        
        if set(self.winnings.keys()) != expected_players:
            logger.error(f"Invalid winnings keys: {set(self.winnings.keys())}, expected {expected_players}")
            raise ValueError(f"Winnings keys must be exactly {expected_players}")
        
        if not all(isinstance(v, int) for v in self.winnings.values()):
            logger.error(f"Invalid winnings values: {self.winnings}, all values must be integers")
            raise ValueError("All winnings values must be integers")
        
        winnings_sum = sum(self.winnings.values())
        if abs(winnings_sum) > 1e-10:  # Allow small tolerance for floating-point errors
            logger.error(f"Winnings do not balance: sum={winnings_sum}, expected 0")
            raise ValueError(f"Winnings do not balance: sum={winnings_sum}, expected 0")
        
        logger.debug(f"Winnings validated successfully: {self.winnings}")