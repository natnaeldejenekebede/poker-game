echo # Poker Game Coding Exercise > README.md
echo. >> README.md
echo A fullstack web application for simulating a 6-player **Texas Hold'em** poker game, built with **FastAPI** (backend), **Next.js** (frontend), and **PostgreSQL** (database). Users can play a hand from preflop to river, log actions, save hands to the database, and view hand history. The project follows the repository pattern, uses the `pokerkit` library for win/loss calculations, and is deployed via **Docker Compose**. >> README.md
echo. >> README.md
echo ## Project Structure >> README.md
echo. >> README.md
echo - `backend/`: **FastAPI** backend with raw SQL repository pattern for hand management. >> README.md
echo   - `pyproject.toml`: **Poetry** configuration for dependencies. >> README.md
echo - `frontend/`: **Next.js** frontend with **TypeScript** and **shadcn/ui** for hand simulation and logging. >> README.md
echo - `docker-compose.yml`: Defines services for database, backend, and frontend. >> README.md
echo - `.env`: Environment variables (not tracked in **Git**). >> README.md
echo - `tests/`: Contains **API** and integration tests. >> README.md
echo. >> README.md
echo ## Features >> README.md
echo. >> README.md
echo - Simulate a 6-player **Texas Hold'em** hand with actions (**Fold**, **Check**, **Call**, **Bet**, **Raise**, **All-in**). >> README.md
echo - Log actions in a text field and display hand history from the database. >> README.md
echo - Calculate winnings using the `pokerkit` library. >> README.md
echo - **RESTful API** with **GET/POST** endpoints for hand resources. >> README.md
echo - Single-page app with game logic separated from **UI** logic. >> README.md
echo - Deployed via **Docker Compose** for easy setup. >> README.md
echo. >> README.md
echo ## Prerequisites >> README.md
echo. >> README.md
echo - [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) >> README.md
echo - [Git](https://git-scm.com/downloads) >> README.md
echo - [Poetry](https://python-poetry.org/docs/#installation) (for **backend** development) >> README.md
echo - [Node.js](https://nodejs.org/) (for **frontend** development) >> README.md
echo. >> README.md
echo ## Setup >> README.md
echo. >> README.md
echo - **Clone the Repository**: >> README.md
echo   ```bash >> README.md
echo   git clone https://github.com/natnaeldejenekebede/poker-game.git >> README.md
echo   cd poker-game >> README.md
echo   ``` >> README.md
echo - **Create `.env` File**: >> README.md
echo   - Create a `.env` file in the project root with the following: >> README.md
echo     ```env >> README.md
echo     POSTGRES_PASSWORD=your_secure_password >> README.md
echo     DATABASE_URL=postgresql://postgres:your_secure_password@db:5432/poker >> README.md
echo     NEXT_PUBLIC_API_URL=http://backend:8000 >> README.md
echo     ``` >> README.md
echo   - Replace `your_secure_password` with a **strong password**. >> README.md
echo - **Start the Application**: >> README.md
echo   ```bash >> README.md
echo   docker compose up -d --build >> README.md
echo   ``` >> README.md
echo - **Access the Application**: >> README.md
echo   - Frontend: [http://localhost:3001](http://localhost:3001) >> README.md
echo   - Backend API: [http://localhost:8000](http://localhost:8000) >> README.md
echo   - Database: `localhost:5433` (use [pgAdmin](https://www.pgadmin.org/) or `psql`) >> README.md
echo. >> README.md
echo ## Usage >> README.md
echo. >> README.md
echo - Start/Reset Hand: Click "Start" (becomes "Reset" after actions) to deal new hands. >> README.md
echo - Take Actions: Use buttons (**Fold**, **Check**, **Call**, **Bet**, **Raise**, **All-in**) to play the hand. Invalid actions are disabled. >> README.md
echo - Adjust Bet/Raise: Use +/- buttons to set amounts in increments of 40 (big blind size). >> README.md
echo - View Logs: Actions appear in the play log (left) in the format `[Player] [Action] [Amount]`. >> README.md
echo - Hand History: Completed hands are saved to the database and displayed (right) with **UUID**, stacks, positions, cards, actions (short format: `f`, `x`, `c`, `bAMOUNT`, `rAMOUNT`, `allin`), and winnings. >> README.md
echo. >> README.md
echo ## Development >> README.md
echo. >> README.md
echo ### Backend (FastAPI with Poetry) >> README.md
echo. >> README.md
echo - **Set Up Poetry Environment**: >> README.md
echo   - Navigate to the backend directory: >> README.md
echo     ```bash >> README.md
echo     cd backend >> README.md
echo     poetry install >> README.md
echo     ``` >> README.md
echo   - Activate the virtual environment: >> README.md
echo     ```bash >> README.md
echo     poetry shell >> README.md
echo     ``` >> README.md
echo   - Alternatively, use `poetry run` for commands without activating the shell. >> README.md
echo - **Edit Code**: >> README.md
echo   - Modify files in `backend/src/` (**FastAPI**, raw **SQL**, `@dataclass`). >> README.md
echo - **Run Tests**: >> README.md
echo   ```bash >> README.md
echo   poetry run pytest >> README.md
echo   ``` >> README.md
echo - **Run Locally** (outside **Docker**, for debugging): >> README.md
echo   ```bash >> README.md
echo   poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 >> README.md
echo   ``` >> README.md
echo   - Ensure the database is running (`docker compose up -d db`). >> README.md
echo - **Apply Changes**: >> README.md
echo   - Rebuild **Docker** image: >> README.md
echo     ```bash >> README.md
echo     docker compose up -d --build backend >> README.md
echo     ``` >> README.md
echo. >> README.md
echo ### Frontend (Next.js) >> README.md
echo. >> README.md
echo - **Install Dependencies**: >> README.md
echo   ```bash >> README.md
echo   cd frontend >> README.md
echo   npm install >> README.md
echo   ``` >> README.md
echo - **Edit Code**: >> README.md
echo   - Modify files in `frontend/` (**Next.js**, **TypeScript**, **shadcn/ui**). >> README.md
echo - **Run Tests**: >> README.md
echo   ```bash >> README.md
echo   npm run test >> README.md
echo   ``` >> README.md
echo - **Run Locally** (outside **Docker**): >> README.md
echo   ```bash >> README.md
echo   npm run dev >> README.md
echo   ``` >> README.md
echo - **Apply Changes**: >> README.md
echo   - Rebuild **Docker** image: >> README.md
echo     ```bash >> README.md
echo     docker compose up -d --build frontend >> README.md
echo     ``` >> README.md
echo. >> README.md
echo ### Database >> README.md
echo. >> README.md
echo - Manage with `psql -h localhost -p 5433 -U postgres -d poker` or [pgAdmin](https://www.pgadmin.org/). >> README.md
echo - Schema: `hands` table with **JSONB** columns for stacks, cards, actions, winnings. >> README.md
echo. >> README.md
echo ## Technical Details >> README.md
echo. >> README.md
echo - **Backend**: >> README.md
echo   - **FastAPI** with raw **SQL** (no **ORM**) and repository pattern. >> README.md
echo   - `@dataclass` for entities. >> README.md
echo   - `pokerkit` for win/loss calculations. >> README.md
echo   - **Poetry** for dependency management (`pyproject.toml`). >> README.md
echo   - **PEP8**-compliant code with **API** tests. >> README.md
echo - **Frontend**: >> README.md
echo   - **Next.js** with **TypeScript** and **shadcn/ui**. >> README.md
echo   - Single-page app with game logic separated from **UI**. >> README.md
echo   - Integration tests for hand simulation. >> README.md
echo - **Database**: >> README.md
echo   - **PostgreSQL** with `hands` table (stores stacks, cards, actions, winnings as **JSONB**). >> README.md
echo - **Deployment**: >> README.md
echo   - **Docker Compose** for database (`postgres:15`), backend, and frontend. >> README.md
echo. >> README.md
echo ## Troubleshooting >> README.md
echo. >> README.md
echo - Database Issues: Verify `.env` matches `docker-compose.yml`. >> README.md
echo - API Errors: Check logs with `docker compose logs backend`. >> README.md
echo - pgAdmin: Connect to `localhost:5433`, database `poker`, user `postgres`. >> README.md
echo - Hand Not Saving: Ensure backend connects to `db:5432` (check logs). >> README.md
echo - Poetry Issues: Ensure **Poetry** is installed (`poetry --version`) and run `poetry install`. >> README.md
echo. >> README.md
echo ## Notes >> README.md
echo. >> README.md
echo - No authentication/authorization required. >> README.md
echo - Layout follows wireframes with **shadcn/ui** styling. >> README.md
echo - Game logic validated on both client and server. >> README.md
echo - Short action format: `f` (**Fold**), `x` (**Check**), `c` (**Call**), `bAMOUNT` (**Bet**), `rAMOUNT` (**Raise**), `allin`. >> README.md
echo. >> README.md
echo ## License >> README.md
echo. >> README.md
echo - MIT License (see `LICENSE` file, if included). >> README.md
