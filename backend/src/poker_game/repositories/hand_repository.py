from uuid import UUID, uuid4
from typing import List, Optional, Dict
import asyncpg
from ..models.hand import Hand
from datetime import datetime
import json

class HandRepository:
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def save(self, hand_data: Dict) -> Dict[str, str]:
        """
        Save hand data to the database and return a dictionary with the hand's ID.
        Generates a UUID if not provided.
        """
        hand_id = hand_data.get("id", str(uuid4()))
        created_at = hand_data.get("created_at", datetime.utcnow())

        # Validate required fields
        required_fields = ["stacks", "player_cards", "action_sequence", "winnings", "dealer_position", "small_blind_position", "big_blind_position"]
        missing_fields = [field for field in required_fields if field not in hand_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        # Validate and prepare data for database
        if not isinstance(hand_data["winnings"], dict):
            raise ValueError(f"Expected 'winnings' to be a dictionary, got: {type(hand_data['winnings'])}")
        if not isinstance(hand_data["action_sequence"], (str, list)):
            raise ValueError(f"Expected 'action_sequence' to be a string or list, got: {type(hand_data['action_sequence'])}")

        query = """
            INSERT INTO hands (id, stacks, dealer_position, small_blind_position, big_blind_position,
                              player_cards, action_sequence, winnings, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
        """
        try:
            # Prepare data with proper serialization
            stacks = json.dumps(hand_data["stacks"])
            player_cards = json.dumps(hand_data["player_cards"])
            action_sequence = hand_data["action_sequence"]
            if isinstance(action_sequence, list):
                action_sequence = json.dumps(action_sequence)
            elif not isinstance(action_sequence, str):
                raise ValueError(f"Invalid action_sequence type after conversion: {type(action_sequence)}")
            winnings_serialized = json.dumps(hand_data["winnings"])

            # Debug: Log query arguments
            print(f"Debug: Saving hand with stacks = {stacks}, type = {type(stacks)}")
            print(f"Debug: Query args: id={hand_id}, stacks={stacks}, dealer_position={hand_data['dealer_position']}, "
                  f"small_blind_position={hand_data['small_blind_position']}, "
                  f"big_blind_position={hand_data['big_blind_position']}, "
                  f"player_cards={player_cards}, "
                  f"action_sequence={action_sequence}, "
                  f"winnings={winnings_serialized}, created_at={created_at}")

            result = await self.connection.fetchrow(
                query,
                UUID(hand_id),
                stacks,
                hand_data["dealer_position"],
                hand_data["small_blind_position"],
                hand_data["big_blind_position"],
                player_cards,
                action_sequence,
                winnings_serialized,
                created_at
            )
            if result is None or "id" not in result:
                raise ValueError("Failed to retrieve ID from database after saving hand")
            return {"id": str(result["id"])}
        except asyncpg.UniqueViolationError:
            raise ValueError(f"Hand with id {hand_id} already exists")
        except asyncpg.DataError as e:
            raise ValueError(f"Invalid data format for database: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to save hand to database: {str(e)}")

    async def find_one_by_id(self, id: UUID) -> Optional[Dict]:
        """Find a Hand by its ID and return a dictionary."""
        query = """
            SELECT id, stacks, dealer_position, small_blind_position, big_blind_position,
                   player_cards, action_sequence, winnings, created_at
            FROM hands WHERE id = $1
        """
        record = await self.connection.fetchrow(query, id)
        if not record:
            return None
        return {
            "id": str(record["id"]),
            "stacks": record["stacks"],
            "dealer_position": record["dealer_position"],
            "small_blind_position": record["small_blind_position"],
            "big_blind_position": record["big_blind_position"],
            "player_cards": record["player_cards"],
            "action_sequence": record["action_sequence"],
            "winnings": record["winnings"],
            "created_at": record["created_at"].isoformat() if record["created_at"] else None
        }

    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve all Hands with pagination and return a list of dictionaries."""
        query = """
            SELECT id, stacks, dealer_position, small_blind_position, big_blind_position,
                   player_cards, action_sequence, winnings, created_at
            FROM hands
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
        """
        records = await self.connection.fetch(query, limit, offset)
        return [
            {
                "id": str(record["id"]),
                "stacks": record["stacks"],
                "dealer_position": record["dealer_position"],
                "small_blind_position": record["small_blind_position"],
                "big_blind_position": record["big_blind_position"],
                "player_cards": record["player_cards"],
                "action_sequence": record["action_sequence"],
                "winnings": record["winnings"],
                "created_at": record["created_at"].isoformat() if record["created_at"] else None
            }
            for record in records
        ]

    async def delete(self, id: UUID) -> None:
        """Delete a Hand by its ID."""
        query = """
            DELETE FROM hands WHERE id = $1
        """
        result = await self.connection.execute(query, id)
        if result == "DELETE 0":
            raise ValueError(f"Hand with id {id} not found")