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

## Match Statistics API

The Statistics API calculates match-level metrics from stored rounds and events. These statistics will be used by the future tactical rule engine.

### Get Match Statistics

```http
GET /matches/{match_id}/statistics
```

Example response:

```json
{
  "match_id": 1,
  "total_rounds": 6,
  "rounds_won": 1,
  "rounds_lost": 4,
  "attack_rounds": 4,
  "defense_rounds": 1,
  "attack_rounds_won": 0,
  "defense_rounds_won": 1,
  "attack_win_rate": 0,
  "defense_win_rate": 1,
  "overall_win_rate": 0.17,
  "spike_plants": 1,
  "post_plant_losses": 1,
  "total_events": 6,
  "event_counts_by_type": {
    "first_death": 3,
    "utility_unused": 2,
    "trade_kill": 1
  },
  "first_death_count": 3,
  "utility_unused_count": 2,
  "trade_kill_count": 1
}
```

### Statistics Currently Calculated

- Total rounds
- Rounds won and lost
- Attack and defense round counts
- Attack, defense, and overall win rates
- Spike plants
- Post-plant losses
- Total gameplay events
- Event counts by type
- First death count
- Utility unused count
- Trade kill count

## Rule-Based Analysis API

The Rule-Based Analysis API converts stored rounds, events, and match statistics into explainable tactical findings. This is the first analysis layer before adding LLM-generated coaching summaries.

### Analyze Match

```http
POST /matches/{match_id}/analyze
```

Example response:

```json
{
  "match_id": 1,
  "total_findings": 6,
  "findings": [
    {
      "issue_type": "repeated_first_deaths",
      "severity": "high",
      "finding": "Player or team recorded 3 first-death events.",
      "evidence": "The match contains 3 first_death events. Repeated first deaths often create early 4v5 disadvantages.",
      "recommendation": "Avoid taking isolated early duels. Use teammate utility, request trade support, or delay first contact until the team is ready to follow up.",
      "confidence": 0.9,
      "round_id": null
    }
  ]
}
```

### Rules Currently Implemented

- Repeated first deaths
- Post-plant conversion issues
- Utility unused in lost rounds
- Low trade support
- Low round conversion

### Why This Layer Exists

The rule engine creates evidence-based findings before the LLM layer is added. This reduces hallucination risk because future AI coaching summaries can be grounded in structured statistics and deterministic findings.

## Persisted Analysis Results API

The backend stores rule-based tactical findings in PostgreSQL so that analysis results can be retrieved later by the dashboard or future LLM coaching layer.

### Run and Save Match Analysis

```http
POST /matches/{match_id}/analyze
```

This endpoint generates rule-based findings and saves them to the `analysis_findings` table.

### Get Saved Match Analysis

```http
GET /matches/{match_id}/analysis
```

Example response:

```json
{
  "match_id": 1,
  "total_findings": 6,
  "findings": [
    {
      "id": 1,
      "match_id": 1,
      "round_id": null,
      "issue_type": "repeated_first_deaths",
      "severity": "high",
      "finding": "Player or team recorded 3 first-death events.",
      "evidence": "The match contains 3 first_death events. Repeated first deaths often create early 4v5 disadvantages.",
      "recommendation": "Avoid taking isolated early duels. Use teammate utility, request trade support, or delay first contact until the team is ready to follow up.",
      "confidence": 0.9,
      "source": "rule_engine",
      "created_at": "2026-05-31T11:51:02.378773Z"
    }
  ]
}
```

### Why This Matters

Persisting analysis results allows the product to support dashboards, historical review, repeated analysis runs, and future LLM-generated summaries grounded in stored evidence.