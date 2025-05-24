# backend/src/poker_game/domain/poker_service.py
from pokerkit import Automation, NoLimitTexasHoldem
from typing import Dict, List
from uuid import uuid4
from datetime import datetime
from ..models.hand import Hand

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
        min_bet: int = 40
    ) -> Hand:
        # Validate input
        if len(stacks) != 6 or len(player_cards) != 6:
            raise ValueError("Exactly 6 players are required")
        if not all(len(cards) == 2 for cards in player_cards):
            raise ValueError("Each player must have exactly 2 hole cards")
        if dealer_position < 0 or dealer_position >= 6:
            raise ValueError("Dealer position must be between 0 and 5")
        if small_blind_position < 0 or small_blind_position >= 6:
            raise ValueError("Small blind position must be between 0 and 5")
        if big_blind_position < 0 or big_blind_position >= 6:
            raise ValueError("Big blind position must be between 0 and 5")

        # Configure blinds for each position
        blinds_or_straddles = [0] * 6  # Initialize for 6 players
        blinds_or_straddles[small_blind_position] = small_blind
        blinds_or_straddles[big_blind_position] = big_blind

        # Initialize game state
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
            ante_trimming_status=False,  # Default: no ante trimming
            raw_antes=0,  # No antes
            raw_blinds_or_straddles=blinds_or_straddles,  # List of blinds per position
            min_bet=min_bet,
            raw_starting_stacks=stacks,
            player_count=6,
            mode=None,  # Default mode
            starting_board_count=1,  # Revert to 1 to satisfy validation
            rake=0,  # No rake
        )

        # Debug: Inspect the State object
        print("State methods and attributes:", dir(state))

        # Deal initial hole cards
        for cards in player_cards:
            state.deal_hole(''.join(cards))  # Assuming pokerkit accepts concatenated cards

        # Track actions and community cards separately
        action_sequence = ["fff"]  # Start with "fff" as required
        current_round = "preflop"
        community_cards = []  # Track flop, turn, river cards separately
        rounds_seen = {"flop": False, "turn": False, "river": False}

        # Process user-provided actions
        for action in actions:
            action_type = action.type
            player_idx = action.player
            amount = action.amount
            cards = action.cards

            if player_idx:
                player_idx = int(player_idx.replace("P", "")) - 1
                if not (0 <= player_idx < 6):
                    raise ValueError(f"Invalid player index: {player_idx + 1}")

            # Debug: Print the current acting player
            print(f"Current acting player index: {state.actor_index}, Processing action for player: {player_idx + 1}")

            # Validate acting player (should start after big blind)
            if state.actor_index != player_idx:
                raise ValueError(f"Player {player_idx + 1} is not acting")

            if action_type in ["fold", "check", "call", "bet", "raise", "allin"]:
                if action_type == "fold":
                    state.fold()  # No player_idx
                    action_sequence.append("f")
                elif action_type == "check":
                    state.check_or_call()  # No player_idx
                    action_sequence.append("x")  # Use "x" for check
                elif action_type == "call":
                    state.check_or_call()  # No player_idx
                    action_sequence.append("c")  # Use "c" for call
                elif action_type == "bet" and amount:
                    if amount < min_bet or amount > state.get_stacks()[state.actor_index]:
                        raise ValueError(f"Invalid bet amount: {amount}")
                    state.complete_bet_or_raise_to(amount)  # No player_idx
                    action_sequence.append(f"b{amount}")
                elif action_type == "raise" and amount:
                    current_bet = state.get_current_bet()
                    if amount < current_bet + min_bet or amount > state.get_stacks()[state.actor_index]:
                        raise ValueError(f"Invalid raise amount: {amount}")
                    state.complete_bet_or_raise_to(amount)  # No player_idx
                    action_sequence.append(f"r{amount}")
                elif action_type == "allin":
                    allin_amount = state.get_stacks()[state.actor_index]
                    state.complete_bet_or_raise_to(allin_amount)  # No player_idx
                    action_sequence.append("allin")  # Simplified to "allin"

            elif action_type in ["flop", "turn", "river"] and cards:
                # Clear any pre-dealt board cards if necessary
                if current_round == "preflop" and action_type == "flop":
                    state.burn_card('??')  # Burn the pre-dealt card from starting_board_count
                elif current_round in ["flop", "turn"]:
                    state.burn_card('??')  # Burn card before dealing turn/river

                # Update round tracking
                if action_type == "flop" and current_round == "preflop":
                    rounds_seen["flop"] = True
                    state.deal_board(*cards.split())
                    community_cards.extend(cards.split())  # Add flop cards
                    current_round = "flop"
                elif action_type == "turn" and current_round == "flop":
                    if not rounds_seen["flop"]:
                        raise ValueError("Flop must occur before turn")
                    rounds_seen["turn"] = True
                    state.deal_board(*cards.split())
                    community_cards.extend(cards.split())  # Add turn card
                    current_round = "turn"
                elif action_type == "river" and current_round == "turn":
                    if not rounds_seen["turn"]:
                        raise ValueError("Turn must occur before river")
                    rounds_seen["river"] = True
                    state.deal_board(*cards.split())
                    community_cards.extend(cards.split())  # Add river card
                    current_round = "river"
                else:
                    raise ValueError(f"Invalid community card stage: {action_type}")

        # If the hand ended early (e.g., all players folded), skip community cards
        if community_cards:
            action_sequence.append("".join(community_cards))  # Append all community cards as a single string

        # Map player IDs and create Hand object
        player_map = {f"P{i+1}": i for i in range(6)}
        stacks_dict = {f"P{i+1}": stack for i, stack in enumerate(state.get_stacks())}
        winnings_dict = {f"P{i+1}": payoff for i, payoff in enumerate(state.get_payoffs())}
        player_cards_dict = {f"P{i+1}": cards for i, cards in enumerate(player_cards)}

        return Hand(
            id=uuid4(),
            stacks=stacks_dict,
            dealer_position=dealer_position,
            small_blind_position=small_blind_position,
            big_blind_position=big_blind_position,
            player_cards=player_cards_dict,
            action_sequence=":".join(action_sequence),  # Use ":" as separator
            winnings=winnings_dict,
            created_at=datetime.now()
        )