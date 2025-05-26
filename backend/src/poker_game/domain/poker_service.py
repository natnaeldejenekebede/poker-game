# backend/src/poker_game/domain/poker_service.py
from pokerkit import Automation, NoLimitTexasHoldem
from typing import Dict, List
from uuid import uuid4
from datetime import datetime
import logging
from ..models.hand import Hand

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    logger.debug(f"Calculating fallback winnings with contributions: {contributions}, winner_idx: {winner_idx}")
    
    # Validate inputs
    if not isinstance(contributions, list) or len(contributions) != 6:
        raise ValueError("Contributions must be a list of 6 integers")
    if not all(isinstance(c, (int, float)) and c >= 0 for c in contributions):
        raise ValueError("All contributions must be non-negative")
    if not (0 <= winner_idx < 6):
        raise ValueError("Winner index must be between 0 and 5")

    total_pot = sum(contributions)
    logger.debug(f"Total pot: {total_pot}")
    if total_pot == 0:
        result = {f"P{i+1}": 0 for i in range(6)}
        logger.debug(f"No pot, returning: {result}")
        return result

    # Initialize winnings with zero, then assign losses and winner's gain
    winnings = {f"P{i+1}": 0 for i in range(6)}

    # Assign losses as negative contributions for all players except the winner
    for i, contrib in enumerate(contributions):
        if i != winner_idx:
            winnings[f"P{i+1}"] = -contrib

    # Winner receives the total pot
    winnings[f"P{winner_idx + 1}"] = total_pot

    # Validate that winnings sum to zero
    winnings_sum = sum(winnings.values())
    if abs(winnings_sum) > 1e-10:  # Allow small tolerance for floating-point errors
        logger.error(f"Winnings do not balance: sum={winnings_sum}, expected 0")
        raise ValueError(f"Winnings do not balance: sum={winnings_sum}, expected 0")

    logger.debug(f"Fallback winnings calculated: {winnings}")
    return winnings

class PokerService:
    @staticmethod
    def calculate_hand(
        stacks: List[int],
        player_cards: List[List[str]],
        actions: List[Dict],
        dealer_position: int,
        small_blind_position: int,
        big_blind_position: int,
        small_blind: int = 20,
        big_blind: int = 40,
        min_bet: int = 20
    ) -> Hand:
        """
        Calculate the outcome of a 6-player Texas Hold'em hand using pokerkit.
        """
        # Validate input
        if len(stacks) != 6 or len(player_cards) != 6:
            raise ValueError("Exactly 6 players are required")
        if not all(len(cards) == 2 for cards in player_cards):
            raise ValueError("Each player must have exactly 2 hole cards")
        if not (0 <= dealer_position < 6 and 0 <= small_blind_position < 6 and 0 <= big_blind_position < 6):
            raise ValueError("Positions must be between 0 and 5")
        if small_blind_position == big_blind_position or dealer_position == small_blind_position:
            raise ValueError("Dealer, small blind, and big blind positions must be unique")

        # Configure blinds for each position
        blinds_or_straddles = [0] * 6
        blinds_or_straddles[small_blind_position] = small_blind
        blinds_or_straddles[big_blind_position] = big_blind

        # Initialize game state with Texas Hold'em settings
        state = NoLimitTexasHoldem.create_state(
            automations=(
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
            ),
            ante_trimming_status=False,
            raw_antes=0,
            raw_blinds_or_straddles=blinds_or_straddles,
            min_bet=min_bet,
            raw_starting_stacks=stacks,
            player_count=6,
            mode=None,
            starting_board_count=1,
            rake=0,
        )

        # Deal initial hole cards
        for cards in player_cards:
            state.deal_hole("".join(cards))

        # Post blinds
        state.complete_bet_or_raise_to(small_blind)
        state.complete_bet_or_raise_to(big_blind)

        # Track actions, community cards, and contributions
        action_sequence = ["fff"]
        current_round = "preflop"
        community_cards = []
        contributions = [0] * 6
        contributions[small_blind_position] += small_blind
        contributions[big_blind_position] += big_blind

        # Process user-provided actions
        for action in actions:
            action_type = action.get("type")
            player_idx = int(action.get("player", f"P{state.actor + 1}").replace("P", "")) - 1 if action.get("player") else state.actor
            amount = action.get("amount")
            cards = action.get("cards")

            if not (0 <= player_idx < 6):
                raise ValueError(f"Invalid player index: {player_idx + 1}")

            if action_type in ["fold", "check", "call", "bet", "raise", "allin"]:
                invested = state.get_invested_amounts()[player_idx] or 0
                current_bet = state.get_current_bet()

                if action_type == "fold":
                    state.fold()
                    action_sequence.append("f")
                elif action_type == "check":
                    if current_bet > invested:
                        raise ValueError("Cannot check with an active bet")
                    state.check_or_call(0)
                    action_sequence.append("x")
                elif action_type == "call":
                    if current_bet <= invested:
                        raise ValueError("Cannot call with no additional bet required")
                    call_amount = min(current_bet - invested, state.get_stacks()[player_idx])
                    state.check_or_call(call_amount)
                    contributions[player_idx] += call_amount
                    action_sequence.append("c")
                elif action_type == "bet" and amount:
                    if amount < min_bet or amount > state.get_stacks()[player_idx]:
                        raise ValueError(f"Invalid bet amount: {amount}")
                    state.complete_bet_or_raise_to(amount)
                    contributions[player_idx] += amount
                    action_sequence.append(f"b{amount}")
                elif action_type == "raise" and amount:
                    if amount <= current_bet or amount > state.get_stacks()[player_idx]:
                        raise ValueError(f"Invalid raise amount: {amount}")
                    additional_amount = amount - invested
                    state.complete_bet_or_raise_to(amount)
                    contributions[player_idx] += additional_amount
                    action_sequence.append(f"r{amount}")
                elif action_type == "allin":
                    allin_amount = state.get_stacks()[player_idx]
                    state.complete_bet_or_raise_to(allin_amount)
                    contributions[player_idx] += allin_amount
                    action_sequence.append("allin")
            elif action_type in ["flop", "turn", "river"] and cards:
                card_list = cards.split()
                if current_round == "preflop" and action_type == "flop" and len(card_list) == 3:
                    state.burn_card()
                    state.deal_board(" ".join(card_list))
                    community_cards.extend(card_list)
                    current_round = "flop"
                elif current_round == "flop" and action_type == "turn" and len(card_list) == 1:
                    state.burn_card()
                    state.deal_board(" ".join(card_list))
                    community_cards.extend(card_list)
                    current_round = "turn"
                elif current_round == "turn" and action_type == "river" and len(card_list) == 1:
                    state.burn_card()
                    state.deal_board(" ".join(card_list))
                    community_cards.extend(card_list)
                    current_round = "river"
                else:
                    raise ValueError(f"Invalid community cards for {action_type}: {cards}")

            if action_type in ["fold", "check", "call", "bet", "raise", "allin"]:
                state.next_actor()

        # Ensure hand completion and showdown
        active_players = [i for i in range(6) if state.get_status()[i] != "folded" and state.get_stacks()[i] > 0]
        if len(active_players) > 1 and current_round == "river":
            state.showdown()
            logger.debug(f"Hand rankings after showdown: {state.get_hand_rankings()}")
        elif len(active_players) == 1:
            state.end_hand()
        else:
            raise ValueError("Hand ended prematurely")

        if community_cards:
            action_sequence.append("".join(community_cards))

        # Calculate winnings
        player_map = {f"P{i+1}": i for i in range(6)}
        stacks_dict = {f"P{i+1}": max(0, stack) for i, stack in enumerate(state.get_stacks())}
        payoffs = state.get_payoffs()
        logger.debug(f"Raw payoffs from pokerkit: {payoffs}")

        # Determine winner (using hand rankings if available)
        winner_idx = None
        if len(active_players) > 1 and current_round == "river":
            rankings = state.get_hand_rankings()
            logger.debug(f"Hand rankings: {rankings}")
            # Find the best hand among active players
            best_rank = float('inf')
            for i in active_players:
                rank = rankings[i] if rankings[i] is not None else float('inf')
                if rank < best_rank:
                    best_rank = rank
                    winner_idx = i
        elif len(active_players) == 1:
            winner_idx = active_players[0]
        else:
            winner_idx = 0  # Default to first player if no active players (shouldn't happen)

        logger.debug(f"Winner index: {winner_idx}")

        # Force fallback calculation for now to bypass pokerkit issues
        logger.warning("Forcing fallback calculation due to persistent issues with pokerkit payoffs")
        winnings_dict = calculate_fallback_winnings(contributions, winner_idx)

        # Validate winnings balance
        winnings_sum = sum(winnings_dict.values())
        if abs(winnings_sum) > 1e-10:
            logger.error(f"Winnings do not balance: sum={winnings_sum}, expected 0")
            raise ValueError("Winnings calculation error: Total winnings/losses must sum to 0")

        # Log for debugging
        logger.debug(f"Contributions: {contributions}")
        logger.debug(f"Total pot: {sum(contributions)}")
        logger.debug(f"Final stacks: {state.get_stacks()}")
        logger.debug(f"Payoffs: {payoffs}")
        logger.debug(f"Winnings: {winnings_dict}")

        player_cards_dict = {f"P{i+1}": cards for i, cards in enumerate(player_cards)}

        # Create Hand object and log its contents
        hand = Hand(
            id=uuid4(),
            stacks=stacks_dict,
            dealer_position=dealer_position,
            small_blind_position=small_blind_position,
            big_blind_position=big_blind_position,
            player_cards=player_cards_dict,
            action_sequence=":".join(action_sequence),
            winnings=winnings_dict,
            created_at=datetime.now()
        )
        logger.debug(f"Hand object created: {vars(hand)}")

        return hand

    @staticmethod
    def format_hand(hand: Hand) -> Dict:
        """
        Format a Hand object into the required Hand History structure.
        """
        logger.debug(f"Formatting hand with winnings: {hand.winnings}")
        action_seq_short = hand.action_sequence.split(":")
        action_seq_short = [a.replace("fff", "").strip() for a in action_seq_short if a]
        formatted = {
            "uuid": str(hand.id),
            "details": (
                f"Stack: {list(hand.stacks.values())[0]}: Dealer: "
                f"Player 1: {' '.join(hand.player_cards['P1'])}; "
                f"Player 2: {' '.join(hand.player_cards['P2'])}; "
                f"Player 3: {' '.join(hand.player_cards['P3'])}; "
                f"Player 4: {' '.join(hand.player_cards['P4'])}"
            ),
            "actions": ";".join(action_seq_short),
            "winnings": {f"Player {k.replace('P', '')}": f"{v:+d}" for k, v in hand.winnings.items()}
        }
        logger.debug(f"Formatted hand: {formatted}")
        return formatted