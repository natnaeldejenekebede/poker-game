import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
from src.poker_game.api.hands import router as hands_router, init_db_pool, close_db_pool
from src.poker_game.db_init import init_db

sys.path.insert(0, str(Path(__file__).parent))

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        import os
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        print(f"Using DATABASE_URL: {database_url}")

        await init_db_pool()
        await init_db()
        print("Database initialized successfully")

        pool = await asyncpg.create_pool(database_url)
        async with pool.acquire() as conn:
            # Verify database connection
            version = await conn.fetchval("SELECT version();")
            print(f"Connected to PostgreSQL: {version}")

            # Check schema for hands table
            schema = await conn.fetch(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'hands'
                """
            )
            print(f"Schema for hands table: {schema}")
        await pool.close()

    except Exception as e:
        print(f"Failed to initialize database: {str(e)}")
        raise
    yield
    try:
        await close_db_pool()
        print("Database pool closed successfully")
    except Exception as e:
        print(f"Failed to close database pool: {str(e)}")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hands_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)