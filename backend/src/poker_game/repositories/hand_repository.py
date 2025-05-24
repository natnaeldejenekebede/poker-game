from uuid import UUID, uuid4
from typing import List, Optional, Dict
import asyncpg
from ..models.hand import Hand
from datetime import datetime

class HandRepository:
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def save(self, hand_data: Dict) -> Dict[str, str]:
        """
        Save hand data to the database and return a dictionary with the hand's ID.
        Generates a UUID if not provided.
        """
        hand_id = hand_data.get("id", uuid4())
        created_at = hand_data.get("created_at", datetime.utcnow())
        
        query = """
            INSERT INTO hands (id, stacks, dealer_position, small_blind_position, big_blind_position,
                              player_cards, action_sequence, winnings, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
        """
        try:
            # Debug: Log query arguments
            stacks = hand_data.get("stacks", [])
            print(f"Debug: Saving hand with stacks = {stacks}, type = {type(stacks)}")
            print(f"Debug: Query args: id={hand_id}, stacks={stacks}, dealer_position={hand_data.get('dealer_position', 0)}, "
                  f"small_blind_position={hand_data.get('small_blind_position', 0)}, "
                  f"big_blind_position={hand_data.get('big_blind_position', 0)}, "
                  f"player_cards={hand_data.get('player_cards', [])}, "
                  f"action_sequence={hand_data.get('action_sequence', [])}, "
                  f"winnings={hand_data.get('winnings', {})}, created_at={created_at}")

            result = await self.connection.fetchrow(
                query,
                hand_id,
                stacks,
                hand_data.get("dealer_position", 0),
                hand_data.get("small_blind_position", 0),
                hand_data.get("big_blind_position", 0),
                hand_data.get("player_cards", []),
                hand_data.get("action_sequence", []),
                hand_data.get("winnings", {}),
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