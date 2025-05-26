# backend/src/poker_game/domain/poker_utils.py
from typing import List, Dict

def calculate_fallback_winnings(contributions: List[int], winner_idx: int) -> Dict[str, int]:
    """
    Calculate winnings as a fallback when pokerkit payoffs are invalid.
    
    Args:
        contributions: List of integers representing each player's total contribution to the pot.
        winner_idx: Index of the winning player (0-5).
    
    Returns:
        Dict[str, int]: Dictionary mapping player IDs (e.g., "P1") to their net winnings/losses.
    
    Raises:
        ValueError: If inputs are invalid (e.g., negative contributions, invalid winner_idx).
    """
    # Validate inputs
    if not isinstance(contributions, list) or len(contributions) != 6:
        raise ValueError("Contributions must be a list of 6 integers")
    if not all(isinstance(c, (int, float)) and c >= 0 for c in contributions):
        raise ValueError("All contributions must be non-negative")
    if not (0 <= winner_idx < 6):
        raise ValueError("Winner index must be between 0 and 5")

    total_pot = sum(contributions)
    if total_pot == 0:
        return {f"P{i+1}": 0 for i in range(6)}  # No pot, no winnings/losses

    # Initialize winnings with negative contributions for all players
    winnings = {f"P{i+1}": -contrib for i, contrib in enumerate(contributions)}

    # Winner receives the full pot, and their contribution is offset
    winner_id = f"P{winner_idx + 1}"
    winnings[winner_id] = total_pot  # Winner gets the entire pot
    winnings[winner_id] += contributions[winner_idx]  # Add back their contribution as a gain

    # Validate that winnings sum to zero
    winnings_sum = sum(winnings.values())
    if abs(winnings_sum) > 1e-10:  # Allow small tolerance for floating-point errors
        raise ValueError(f"Winnings do not balance: sum={winnings_sum}, expected 0")

    return winnings