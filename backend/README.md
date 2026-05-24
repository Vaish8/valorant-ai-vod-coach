# Backend API

FastAPI backend for the Valorant AI VOD Coach project.

## Current Features

- FastAPI application setup
- Health check endpoint
- Database health check endpoint
- Environment-based configuration
- CORS middleware for frontend integration
- PostgreSQL database connection using SQLAlchemy
- Redis service available through Docker Compose
- Match session API for creating and retrieving Valorant VOD review sessions
- Round API for storing round-level match data
- Event API for storing structured gameplay events
- Automatic API documentation via Swagger UI

## Tech Stack

- FastAPI
- Python
- SQLAlchemy
- PostgreSQL
- Redis
- Docker Compose
- Pydantic
- Uvicorn
- psycopg

## Run Locally

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

## Database Setup

This backend uses PostgreSQL with SQLAlchemy.

### Start PostgreSQL and Redis

From the project root:

```bash
docker compose up -d db redis
```

### Database Health Check

```http
GET /db/health
```

Expected response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

## Match Session API

The Match API stores Valorant match/VOD review sessions in PostgreSQL.

### Create Match Session

```http
POST /matches
```

Example request:

```json
{
  "title": "Ranked Ascent VOD Review",
  "map_name": "Ascent",
  "player_agent": "Jett",
  "rank": "Gold 2"
}
```

Example response:

```json
{
  "id": 1,
  "title": "Ranked Ascent VOD Review",
  "map_name": "Ascent",
  "player_agent": "Jett",
  "rank": "Gold 2",
  "vod_file_path": null,
  "video_duration_seconds": null,
  "video_fps": null,
  "video_resolution": null,
  "created_at": "2026-05-24T16:04:19.878511Z",
  "updated_at": "2026-05-24T16:04:19.878515Z"
}
```

### List Match Sessions

```http
GET /matches
```

### Get Match Session by ID

```http
GET /matches/{match_id}
```

### Match Error Handling

If a match does not exist:

```json
{
  "detail": "Match with id 999 not found"
}
```

## Round and Event API

The Round and Event APIs store structured gameplay data for each match session. These records will later power rule-based tactical analysis and AI coaching feedback.

Current relationship:

```text
Match
   |
   v
Round
   |
   v
Event
```

### Create Round for Match

```http
POST /matches/{match_id}/rounds
```

Example request:

```json
{
  "round_number": 1,
  "side": "attack",
  "round_result": "lost",
  "spike_planted": false,
  "site": null,
  "start_time_seconds": 0,
  "end_time_seconds": 95
}
```

Example response:

```json
{
  "id": 1,
  "match_id": 1,
  "round_number": 1,
  "side": "attack",
  "round_result": "lost",
  "spike_planted": false,
  "site": null,
  "start_time_seconds": 0,
  "end_time_seconds": 95,
  "created_at": "2026-05-24T16:50:28.905233Z"
}
```

### List Rounds for Match

```http
GET /matches/{match_id}/rounds
```

### Create Event for Round

```http
POST /rounds/{round_id}/events
```

Example request:

```json
{
  "timestamp_seconds": 32,
  "event_type": "first_death",
  "actor": "self",
  "target": null,
  "location": "mid",
  "description": "Player died first while peeking mid without trade support.",
  "source": "manual",
  "confidence": 1.0
}
```

Example response:

```json
{
  "id": 1,
  "round_id": 1,
  "timestamp_seconds": 32,
  "event_type": "first_death",
  "actor": "self",
  "target": null,
  "location": "mid",
  "description": "Player died first while peeking mid without trade support.",
  "source": "manual",
  "confidence": 1.0,
  "created_at": "2026-05-24T16:53:59.485509Z"
}
```

### List Events for Round

```http
GET /rounds/{round_id}/events
```

### Round and Event Error Handling

If a match does not exist:

```json
{
  "detail": "Match with id 999 not found"
}
```

If a round does not exist:

```json
{
  "detail": "Round with id 999 not found"
}
```

If a round exists but has no events, the API returns an empty list:

```json
[]
```

## Development Notes

The current MVP uses SQLAlchemy `create_all()` during development to create database tables automatically. This will later be replaced with Alembic migrations for production-grade schema management.

The current event input is manual/structured. This is intentional for the MVP because it creates reliable data for the future rule-based tactical analysis engine before adding video-processing automation.

## Database Stack

- PostgreSQL
- SQLAlchemy
- psycopg
- Redis
- Docker Compose