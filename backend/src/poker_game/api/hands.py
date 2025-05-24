from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from uuid import UUID
from typing import List, Dict, Optional
import asyncpg
import os
from ..models.hand import Hand
from ..repositories.hand_repository import HandRepository
from ..domain.poker_service import PokerService

router = APIRouter(prefix="/hands", tags=["hands"])

# Global database pool (to be initialized in main.py)
db_pool: Optional[asyncpg.Pool] = None

# Pydantic model for action validation
class Action(BaseModel):
    type: str
    player: Optional[str] = None
    amount: Optional[int] = None
    cards: Optional[str] = None

    @validator('type')
    def validate_action_type(cls, v):
        valid_types = ["fold", "check", "call", "bet", "raise", "allin", "flop", "turn", "river"]
        if v not in valid_types:
            raise ValueError(f"Action type must be one of {valid_types}")
        return v

    @validator('amount')
    def validate_amount(cls, v, values):
        if 'type' in values and values['type'] in ["bet", "raise"] and (v is None or v <= 0):
            raise ValueError(f"Amount must be provided and greater than 0 for {values['type']}")
        return v

    @validator('cards')
    def validate_cards_field(cls, v, values):
        if 'type' in values and values['type'] in ["flop", "turn", "river"] and v is None:
            raise ValueError(f"Cards must be provided for {values['type']}")
        return v

# Pydantic model for input validation
class HandCreateRequest(BaseModel):
    stacks: List[int]
    player_cards: List[List[str]]
    actions: List[Action]
    dealer_position: int
    small_blind_position: int
    big_blind_position: int
    winnings: Optional[dict] = None

    @validator('player_cards')
    def validate_cards(cls, v):
        for cards in v:
            if len(cards) != 2:
                raise ValueError("Each player must have exactly 2 cards")
        if len(v) != 6:
            raise ValueError("Exactly 6 players are required")
        return v

    @validator('stacks')
    def validate_stacks(cls, v, values):
        if 'player_cards' in values and len(v) != len(values['player_cards']):
            raise ValueError("Number of stacks must match number of players (6)")
        return v

    @validator('dealer_position')
    def validate_dealer_position(cls, v):
        if not (0 <= v <= 5):
            raise ValueError("Dealer position must be between 0 and 5")
        return v

    @validator('small_blind_position')
    def validate_small_blind_position(cls, v, values):
        if not (0 <= v <= 5):
            raise ValueError("Small blind position must be between 0 and 5")
        if 'dealer_position' in values:
            expected_small_blind = (values['dealer_position'] + 1) % 6
            if v != expected_small_blind:
                raise ValueError(f"Small blind position must be one position after dealer (expected {expected_small_blind})")
        return v

    @validator('big_blind_position')
    def validate_big_blind_position(cls, v, values):
        if not (0 <= v <= 5):
            raise ValueError("Big blind position must be between 0 and 5")
        if 'small_blind_position' in values:
            expected_big_blind = (values['small_blind_position'] + 1) % 6
            if v != expected_big_blind:
                raise ValueError(f"Big blind position must be one position after small blind (expected {expected_big_blind})")
        return v

# Pydantic model for POST response
class HandCreateResponse(BaseModel):
    id: UUID

# Function to initialize the pool (called in main.py)
async def init_db_pool():
    global db_pool
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        print(f"Initializing db_pool with DATABASE_URL: {database_url}")
        db_pool = await asyncpg.create_pool(
            database_url,
            min_size=2,
            max_size=10
        )
        if db_pool is None:
            raise ValueError("Failed to create database pool")
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {str(e)}")

# Function to close the pool (called on shutdown in main.py)
async def close_db_pool():
    global db_pool
    if db_pool is not None:
        await db_pool.close()

# Dependency to get the shared database pool
async def get_db_pool() -> asyncpg.Pool:
    if db_pool is None:
        raise HTTPException(
            status_code=500,
            detail="Database pool not initialized"
        )
    return db_pool

@router.post("/create", response_model=HandCreateResponse, status_code=201)
async def create_hand(
    hand_data: HandCreateRequest,
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    try:
        positions = [
            hand_data.dealer_position,
            hand_data.small_blind_position,
            hand_data.big_blind_position
        ]
        if not (positions == sorted(set(positions))):
            raise ValueError("Positions must be unique and in dealer → small blind → big blind order")
        
        # Use provided winnings if available, otherwise calculate
        winnings = hand_data.winnings if hand_data.winnings is not None else {}
        if not winnings:
            last_action = hand_data.actions[-1] if hand_data.actions else None
            if last_action and last_action.type == "fold" and len(hand_data.actions) > 1:
                winner = hand_data.actions[-2].player if hand_data.actions[-2].player != last_action.player else None
                if winner:
                    pot = sum([action.amount or 0 for action in hand_data.actions if action.type in ["call", "bet", "raise"]])
                    winnings = {winner: pot}

        # Convert Action objects to dictionaries for JSONB storage
        action_sequence = [action.dict(exclude_unset=True) for action in hand_data.actions]

        # Prepare data for repository
        hand_data_dict = {
            "stacks": hand_data.stacks,
            "player_cards": hand_data.player_cards,
            "action_sequence": action_sequence,
            "winnings": winnings,
            "dealer_position": hand_data.dealer_position,
            "small_blind_position": hand_data.small_blind_position,
            "big_blind_position": hand_data.big_blind_position
        }

        # Debug: Log hand_data_dict
        print(f"Debug: hand_data_dict = {hand_data_dict}, stacks type = {type(hand_data_dict['stacks'])}")

        # Save to database
        async with pool.acquire() as conn:
            repo = HandRepository(conn)
            saved_hand = await repo.save(hand_data_dict)
            print(f"Debug: saved_hand = {saved_hand}, type = {type(saved_hand)}")
            if not isinstance(saved_hand, dict):
                raise ValueError(f"Expected a dictionary from HandRepository.save(), got: {type(saved_hand)}")
            hand_id = saved_hand.get("id")
            if hand_id is None:
                raise ValueError(f"HandRepository.save() did not return an 'id' key. Got: {saved_hand}")
            return JSONResponse(content={"id": hand_id}, status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=List[Dict])
async def get_hands(
    limit: int = 100,
    offset: int = 0,
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    try:
        async with pool.acquire() as conn:
            repo = HandRepository(conn)
            hands = await repo.find_all(limit, offset)
            return hands
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")