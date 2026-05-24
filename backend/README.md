# Backend API

FastAPI backend for the Valorant AI VOD Coach project.

## Current Features

- FastAPI application setup
- Health check endpoint
- Environment-based configuration
- CORS middleware for frontend integration
- Automatic API documentation via Swagger UI

## Run Locally

Create and activate virtual environment:

```bash
python -m venv venv

## Database Setup

This backend uses PostgreSQL with SQLAlchemy.

### Start PostgreSQL and Redis

From the project root:

```bash
docker compose up -d db redis
```

### Run Backend Locally

From the backend folder:

```bash
python -m uvicorn app.main:app --reload
```

### Database Health Check

```bash
GET /db/health
```

Expected response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

## Database Stack

- PostgreSQL
- SQLAlchemy
- psycopg
- Redis
- Docker Compose