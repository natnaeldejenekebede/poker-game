FROM python:3.12-slim

WORKDIR /app

# Set Python path to include /app
ENV PYTHONPATH=/app

# Install system dependencies for PostgreSQL client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN pip install --upgrade pip --retries 3 --timeout 60 && \
    pip install poetry --retries 3 --timeout 60 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi
    
# Copy the rest of the application
COPY . .

# Install the project package
RUN poetry install --no-interaction --no-ansi

# Run from the correct module path
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]