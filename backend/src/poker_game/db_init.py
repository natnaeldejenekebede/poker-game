from typing import Optional
import asyncpg
import asyncio
import os

async def init_db(pool: Optional[asyncpg.Pool] = None) -> None:
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        local_pool = pool or await asyncpg.create_pool(database_url)
        if local_pool is None:
            raise ValueError("Failed to create database pool")

        async with local_pool.acquire() as conn:
            # Check if table exists
            table_exists = await conn.fetchval(
                "SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'hands')"
            )

            if not table_exists:
                # Apply migration script if table doesn't exist
                migration_path = os.path.join(os.path.dirname(__file__), "../../migrations/001_create_hands_table.sql")
                if not os.path.exists(migration_path):
                    raise ValueError(f"Migration script not found at {migration_path}")

                with open(migration_path, 'r') as f:
                    script_content = f.read()
                    if not script_content.strip():
                        raise ValueError("Migration script is empty")
                    await conn.execute(script_content)
            else:
                # Check column types and alter if necessary
                column_types = await conn.fetch(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'hands'
                    AND column_name IN ('stacks', 'player_cards', 'action_sequence', 'winnings')
                    """
                )
                for column in column_types:
                    if column['data_type'].lower() != 'jsonb':
                        await conn.execute(f"""
                            ALTER TABLE hands
                            ALTER COLUMN {column['column_name']} TYPE JSONB
                            USING {column['column_name']}::JSONB
                        """)
                        print(f"Altered column {column['column_name']} to JSONB")

        if pool is None:
            await local_pool.close()

    except asyncpg.PostgresError as e:
        raise ValueError(f"Database error during initialization: {str(e)}")
    except IOError as e:
        raise ValueError(f"Error reading migration script: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during database initialization: {str(e)}")

if __name__ == "__main__":
    asyncio.run(init_db())