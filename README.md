echo # Poker Game > README.md
echo. >> README.md
echo A web-based poker game built with FastAPI (backend), Next.js (frontend), and PostgreSQL (database). The application simulates poker hands, storing game data such as stacks, player cards, actions, and winnings. >> README.md
echo. >> README.md
echo ## Project Structure >> README.md
echo. >> README.md
echo - `backend/`: FastAPI backend for handling game logic and database interactions. >> README.md
echo - `frontend/`: Next.js frontend for the user interface. >> README.md
echo - `docker-compose.yml`: Defines services for the database, backend, and frontend. >> README.md
echo - `.env`: Environment variables (not tracked in Git). >> README.md
echo. >> README.md
echo ## Prerequisites >> README.md
echo. >> README.md
echo - Docker and Docker Compose >> README.md
echo - Git >> README.md
echo - Node.js (for frontend development) >> README.md
echo - Python 3.8+ (for backend development) >> README.md
echo. >> README.md
echo ## Setup >> README.md
echo. >> README.md
echo 1. **Clone the Repository**: >> README.md
echo    ```bash >> README.md
echo    git clone https://github.com/natnaeldejenekebede/poker-game.git >> README.md
echo    cd poker-game >> README.md
echo    ``` >> README.md
echo. >> README.md
echo 2. **Create `.env` File**: >> README.md
echo    Create a `.env` file in the project root with the following variables: >> README.md
echo    ```env >> README.md
echo    POSTGRES_PASSWORD=your_secure_password >> README.md
echo    DATABASE_URL=postgresql://postgres:your_secure_password@db:5432/poker >> README.md
echo    NEXT_PUBLIC_API_URL=http://backend:8000 >> README.md
echo    ``` >> README.md
echo    Replace `your_secure_password` with a strong password. >> README.md
echo. >> README.md
echo 3. **Start the Application**: >> README.md
echo    ```bash >> README.md
echo    docker compose up -d --build >> README.md
echo    ``` >> README.md
echo. >> README.md
echo 4. **Access the Application**: >> README.md
echo    - Frontend: `http://localhost:3001` >> README.md
echo    - Backend API: `http://localhost:8000` >> README.md
echo    - Database: `localhost:5433` (use pgAdmin or psql) >> README.md
echo. >> README.md
echo ## Usage >> README.md
echo. >> README.md
echo - Use the frontend to interact with the poker game. >> README.md
echo - Send POST requests to `http://localhost:8000/hands/create` to create new hands (see API documentation in `backend/`). >> README.md
echo. >> README.md
echo ## Development >> README.md
echo. >> README.md
echo - **Backend**: Edit files in `backend/src/`. Run `docker compose up --build` to apply changes. >> README.md
echo - **Frontend**: Edit files in `frontend/`. Run `docker compose up --build` to apply changes. >> README.md
echo - **Database**: Use pgAdmin or `psql -h localhost -p 5433 -U postgres -d poker` to manage the database. >> README.md
echo. >> README.md
echo ## Troubleshooting >> README.md
echo. >> README.md
echo - **Database Issues**: Ensure `.env` variables match `docker-compose.yml`. >> README.md
echo - **API Errors**: Check backend logs with `docker compose logs backend`. >> README.md
echo - **pgAdmin**: Connect to `localhost:5433`, database `poker`, user `postgres`. >> README.md
echo. >> README.md
echo ## License >> README.md
echo. >> README.md
echo MIT License (see `LICENSE` file, if included). >> README.md
