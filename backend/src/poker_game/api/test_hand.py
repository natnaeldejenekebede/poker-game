# backend/tests/poker_game/api/test_hands.py
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from src.poker_game.api.hands import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_create_and_get_hand():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create hand
        hand_data = {
            "stacks": [1000] * 6,
            "player_cards": [["Tc", "2c"], ["5d", "4c"], ["Ah", "4s"], ["Qc", "Td"], ["Js", "9d"], ["8h", "6s"]],
            "actions": [
                {"type": "fold", "player": "P3"},
                {"type": "call", "player": "P1"},
                {"type": "flop", "cards": "3hKdQs"},
                {"type": "check", "player": "P1"}
            ],
            "dealer_position": 0,
            "small_blind_position": 1,
            "big_blind_position": 2
        }
        create_response = await client.post("/hands", json=hand_data)
        assert create_response.status_code == 200
        hand_id = create_response.json()

        # Get hands
        get_response = await client.get("/hands")
        assert get_response.status_code == 200
        hands = get_response.json()
        assert len(hands) > 0
        assert hands[0]["id"] == str(hand_id)