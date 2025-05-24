**Poker Game Coding Exercise**

A fullstack web application for simulating a 6-player Texas Hold'em poker game, built with FastAPI (backend), Next.js (frontend), and PostgreSQL (database). Users can play a hand from preflop to river, log actions, save hands to the database, and view hand history. The project follows the repository pattern, uses the pokerkit library for win/loss calculations, and is deployed via Docker Compose.

**Project Structure**

backend/: FastAPI backend with raw SQL repository pattern for hand management.
pyproject.toml: Poetry configuration for dependencies.


frontend/: Next.js frontend with TypeScript and shadcn/ui for hand simulation and logging.
docker-compose.yml: Defines services for database, backend, and frontend.
.env: Environment variables (not tracked in Git).
tests/: Contains API and integration tests.

Features

Simulate a 6-player Texas Hold'em hand with actions (Fold, Check, Call, Bet, Raise, All-in).
Log actions in a text field and display hand history from the database.
Calculate winnings using the pokerkit library.
RESTful API with GET/POST endpoints for hand resources.
Single-page app with game logic separated from UI logic.
Deployed via Docker Compose for easy setup.

Prerequisites

Docker and Docker Compose
Git
Poetry (for backend development)
Node.js (for frontend development)

Setup

Clone the Repository:
git clone https://github.com/natnaeldejenekebede/poker-game.git
cd poker-game


Create .env File:Create a .env file in the project root with the following:
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://postgres:your_secure_password@db:5432/poker
NEXT_PUBLIC_API_URL=http://backend:8000

Replace your_secure_password with a strong password.

Start the Application:
docker compose up -d --build


Access the Application:

Frontend: http://localhost:3001
Backend API: http://localhost:8000
Database: localhost:5433 (use pgAdmin or psql)



Usage

Start/Reset Hand: Click "Start" (becomes "Reset" after actions) to deal new hands.
Take Actions: Use buttons (Fold, Check, Call, Bet, Raise, All-in) to play the hand. Invalid actions are disabled.
Adjust Bet/Raise: Use +/- buttons to set amounts in increments of 40 (big blind size).
View Logs: Actions appear in the play log (left) in the format [Player] [Action] [Amount].
Hand History: Completed hands are saved to the database and displayed (right) with UUID, stacks, positions, cards, actions (short format: f, x, c, bAMOUNT, rAMOUNT, allin), and winnings.

Development
Backend (FastAPI with Poetry)

Set Up Poetry Environment:Navigate to the backend directory:
cd backend
poetry install

Activate the virtual environment:
poetry shell

Alternatively, use poetry run for commands without activating the shell.

Edit Code:Modify files in backend/src/ (FastAPI, raw SQL, @dataclass).

Run Tests:
poetry run pytest


Run Locally (outside Docker, for debugging):
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000

Ensure the database is running (docker compose up -d db).

Apply Changes:Rebuild Docker image:
docker compose up -d --build backend



Frontend (Next.js)

Install Dependencies:
cd frontend
npm install


Edit Code:Modify files in frontend/ (Next.js, TypeScript, shadcn/ui).

Run Tests:
npm run test


Run Locally (outside Docker):
npm run dev


Apply Changes:Rebuild Docker image:
docker compose up -d --build frontend



Database

Manage with psql -h localhost -p 5433 -U postgres -d poker or pgAdmin.
Schema: hands table with JSONB columns for stacks, cards, actions, winnings.

Technical Details

Backend:
FastAPI with raw SQL (no ORM) and repository pattern.
@dataclass for entities.
pokerkit for win/loss calculations.
Poetry for dependency management (pyproject.toml).
PEP8-compliant code with API tests.


Frontend:
Next.js with TypeScript and shadcn/ui.
Single-page app with game logic separated from UI.
Integration tests for hand simulation.


Database: PostgreSQL with hands table (stores stacks, cards, actions, winnings as JSONB).
Deployment: Docker Compose for database (postgres:15), backend, and frontend.

Troubleshooting

Database Issues: Verify .env matches docker-compose.yml.
API Errors: Check logs with docker compose logs backend.
pgAdmin: Connect to localhost:5433, database poker, user postgres.
Hand Not Saving: Ensure backend connects to db:5432 (check logs).
Poetry Issues: Ensure Poetry is installed (poetry --version) and run poetry install.

Notes

No authentication/authorization required.
Layout follows wireframes with shadcn/ui styling.
Game logic validated on both client and server.
Short action format: f (Fold), x (Check), c (Call), bAMOUNT (Bet), rAMOUNT (Raise), allin.

License
MIT License (see LICENSE file, if included).
