Fullstack Poker Coding Exercise
This project implements a fullstack Texas Hold'em Poker game with a React/Next.js frontend, a FastAPI backend, and a PostgreSQL database. The application allows users to play poker hands, perform actions (e.g., fold, check), and view hand history, all while storing game data in a database.
Project Structure

backend/: FastAPI backend with endpoints for creating and retrieving poker hands.
frontend/: Next.js frontend for the poker game UI.
docker-compose.yml: Docker configuration for running the backend, frontend, and database.

Prerequisites
Before setting up the project, ensure you have the following installed:

Python 3.12: For the backend (FastAPI).
Node.js 18: For the frontend (Next.js).
Docker and Docker Compose: To containerize the application.
Poetry: For Python dependency management.
Windows PowerShell: For running commands (or another terminal if on a different OS).
VirtualBox (Optional): If using Docker with VirtualBox instead of Docker Desktop (not required for your setup).

Setup Instructions
1. Clone the Repository
Clone the project to your local machine:
git clone <repository-url>
cd poker-game

2. Backend Setup with Poetry
Install Poetry
Install Poetry for dependency management:
curl -sSL https://install.python-poetry.org | python3 -

Add Poetry to your PATH (if not already added):

On Windows, add C:\Users\HP\AppData\Roaming\Python\Scripts to your PATH.

Create and Activate Virtual Environment
Navigate to the backend directory:
cd backend

Install dependencies and activate the virtual environment:
poetry install
poetry shell

This activates the virtual environment (e.g., poker-backend-py3.12).
Verify Backend Dependencies
Ensure dependencies like fastapi, uvicorn, and psycopg2 are installed:
poetry show

3. Frontend Setup (Optional Local Development)
Navigate to Frontend Directory
If you want to run the frontend locally (outside Docker) for development:
cd ../frontend

Install Dependencies
Install Node.js dependencies:
npm install

Run Locally (Optional)
Run the frontend in development mode:
npm run dev

This starts the Next.js app on http://localhost:3000. However, we’ll use Docker for production.
4. Docker Setup
Install Docker

Windows: Install Docker Desktop from https://www.docker.com/products/docker-desktop/.
Ensure WSL 2 or Hyper-V is enabled.
During installation, enable Docker Compose support.


Notes:
backend: FastAPI app on port 8000.
frontend: Next.js app on port 3001 (mapped to 3000 in the container).
db: PostgreSQL database with persistent data.



Build and Run with Docker
From the project root (C:\Users\HP\Documents\FastAPI\poker-game):
docker compose up -d --build


-d: Runs in detached mode.
--build: Builds the images before starting.

Verify Containers
Check the status of the containers:
docker compose ps

Expected Output:
NAME                    IMAGE                 COMMAND                  SERVICE    STATUS                   PORTS
poker-game-backend-1    poker-game-backend    "uvicorn main:app --…"   backend    Up                       0.0.0.0:8000->8000/tcp
poker-game-db-1         postgres:15           "docker-entrypoint.s…"   db         Up (healthy)             0.0.0.0:5433->5432/tcp
poker-game-frontend-1   poker-game-frontend   "docker-entrypoint.s…"   frontend   Up                       0.0.0.0:3001->3000/tcp

Check Logs
Verify the backend and frontend started correctly:
docker compose logs backend
docker compose logs frontend


Backend Expected: INFO: Uvicorn running on http://0.0.0.0:8000.
Frontend Expected: ✓ Ready in 17s.

5. VirtualBox Setup (Optional)
If you’re using Docker with VirtualBox instead of Docker Desktop:

Install VirtualBox: Download and install from https://www.virtualbox.org/.
Install Docker Toolbox:
Download Docker Toolbox for Windows (older versions support VirtualBox).
Follow the installation instructions.


Run Docker with VirtualBox:
Start the Docker Quickstart Terminal (sets up a VirtualBox VM).
Run Docker commands as above from the terminal.



Note: Since you’re using Docker Desktop, this step is not necessary for your setup.
6. Access the Application

Backend: http://localhost:8000
API endpoints:
POST /hands/create: Create a new poker hand.
GET /hands/: Retrieve hand history.




Frontend: http://localhost:3001
Play a game, perform actions (fold, check), and view hand history.



7. Testing with Postman
Test POST /hands/create

Method: POST
URL: http://localhost:8000/hands/create
Headers: Content-Type: application/json
Body:{
  "stacks": [1125600, 1125600, 1125600, 1125600, 1125600, 1125600],
  "player_cards": [["Ac", "Ad"], ["Kc", "Kd"], ["Qc", "Qd"], ["Jc", "Jd"], ["Tc", "Td"], ["9c", "9d"]],
  "actions": [{"type": "fold", "player": "P1"}],
  "dealer_position": 0,
  "small_blind_position": 1,
  "big_blind_position": 2
}


Expected: 201 Created, {"id": "some-uuid-here"}.

Test GET /hands/

Method: GET
URL: http://localhost:8000/hands/
Query Params: limit=10, offset=0
Expected: 200 OK, list of hands.

8. Troubleshooting
Port Conflicts

Check if ports 8000 or 3001 are in use:Get-NetTCPConnection -LocalPort 3001


Stop conflicting processes:Stop-Process -Id <PID> -Force


Or change ports in docker-compose.yml (e.g., 3002:3000).

Backend Errors

Check logs: docker compose logs backend.
Ensure database connection: Verify DATABASE_URL.

Frontend Errors

Check logs: docker compose logs frontend.
Ensure .next directory exists after build.

9. Next Steps

Improve Code:
Replace eval() in HandRepository with JSON.parse/JSON.stringify.
Add zod validation in the frontend.


Add Tests:
Backend: Use pytest for API tests.
Frontend: Use Cypress for end-to-end tests.


Finalize:
Package the repository (exclude node_modules and virtual environments).



10. Notes

Environment: Tested on Windows with Docker Desktop.
Plagiarism Warning: Ensure all work is your own per exercise guidelines.
Last Updated: May 21, 2025.































# Python
__pycache__/
*.py[cod]
*$py.class
*.pyc
*.pyd
.Python
env/
venv/
.env
*.env
.venv/
poetry.lock  # Keep this if you want to version it; remove if managed separately
# Note: poetry.lock is included by default in some projects; adjust based on your workflow

# Backend-specific
backend/__pycache__/
backend/.venv/
backend/*.log
backend/*.sqlite

# Frontend (NextJS)
frontend/node_modules/
frontend/.next/
frontend/out/
frontend/build/
frontend/dist/
frontend/*.log
frontend/.env
frontend/.env.local
frontend/.env.*.local

# Docker
Dockerfile
docker-compose.yml  # Keep this if you want it versioned; remove if sensitive
docker-compose.override.yml
.Dockerignore
*.dockerignore
!backend/.dockerignore  # Keep backend-specific .dockerignore if exists
!frontend/.dockerignore  # Keep frontend-specific .dockerignore if exists
docker/
*.tar

# Logs and databases
*.log
*.sql
*.sqlite

# OS-generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Editor and IDE files
.idea/
.vscode/
*.sublime-workspace
*.sublime-project

# macOS
*.swp

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini

# Virtual machine and container files
.vagrant/
*.vdi
*.vmdk
*.vmx

# Miscellaneous
*.pyc
*.pyo
*.pyd
.Python
build/
dist/
*.egg-info/
.installed.cfg
*.egg

# Local configuration
config.yml
config.json
local_settings.py

# Test artifacts
.coverage
htmlcov/
.tox/
.nox/
.cache/
pytest_cache/
.pytest_cache/

# Ignore migration backups (if any)
migrations/backup/
