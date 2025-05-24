Poker Game
A web-based poker game built with FastAPI (backend), Next.js (frontend), and PostgreSQL (database). The application simulates poker hands, storing game data such as stacks, player cards, actions, and winnings.
Project Structure

backend/: FastAPI backend for handling game logic and database interactions.
frontend/: Next.js frontend for the user interface.
docker-compose.yml: Defines services for the database, backend, and frontend.
.env: Environment variables (not tracked in Git).

Prerequisites

Docker and Docker Compose
Git
Node.js (for frontend development)
Python 3.8+ (for backend development)

Setup

Clone the Repository:
git clone https://github.com/natnaeldejenekebede/poker-game.git
cd poker-game


Create .env File:Create a .env file in the project root with the following variables:
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

Use the frontend to interact with the poker game.
Send POST requests to http://localhost:8000/hands/create to create new hands (see API documentation in backend/).

Development

Backend: Edit files in backend/src/. Run docker compose up --build to apply changes.
Frontend: Edit files in frontend/. Run docker compose up --build to apply changes.
Database: Use pgAdmin or psql -h localhost -p 5433 -U postgres -d poker to manage the database.

Troubleshooting

Database Issues: Ensure .env variables match docker-compose.yml.
API Errors: Check backend logs with docker compose logs backend.
pgAdmin: Connect to localhost:5433, database poker, user postgres.

License
MIT License (see LICENSE file, if included).
