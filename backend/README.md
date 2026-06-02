# Backend API

FastAPI backend for the Valorant AI VOD Coach project.

## Current Features

* FastAPI application setup
* Health check endpoint
* Database health check endpoint
* Environment-based configuration
* CORS middleware for frontend integration
* PostgreSQL database connection using SQLAlchemy
* Redis service available through Docker Compose
* Alembic database migrations for version-controlled schema management
* Match session API for creating and retrieving Valorant VOD review sessions
* Round API for storing round-level match data
* Event API for storing structured gameplay events
* Match statistics API for calculating gameplay metrics
* Rule-based tactical analysis API for generating explainable findings
* Persisted analysis results stored in PostgreSQL
* Enum-based validation for structured gameplay data
* Automated API documentation via Swagger UI
* Automated backend tests using `pytest` and FastAPI `TestClient`
* Coach summary API for generating match-level coaching output from saved findings

## Demo Data

Sample request and response payloads are available in the root `sample_data/` directory.

Current sample files include:

* `sample_match_payload.json`
* `sample_rounds_payload.json`
* `sample_events_payload.json`
* `sample_statistics_response.json`
* `sample_analysis_response.json`

A complete demo workflow is documented in:

```text
docs/demo-workflow.md
```

## Tech Stack

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL
* Redis
* Docker Compose
* Pydantic
* Uvicorn
* psycopg
* Alembic
* pytest
* httpx
* GitHub Actions

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

Start PostgreSQL and Redis from the project root:

```bash
docker compose up -d db redis
```

Apply database migrations from the `backend/` folder:

```bash
alembic upgrade head
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

## Database Migrations

This backend uses Alembic for version-controlled PostgreSQL schema migrations.

Create a new migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe schema change"
```

Apply migrations:

```bash
alembic upgrade head
```

Check the current migration version:

```bash
alembic current
```

The initial migration creates the core backend tables:

* `matches`
* `rounds`
* `events`
* `analysis_findings`

During early development and testing, the backend still includes an `init_db()` helper for creating tables automatically. Production-style schema changes should be managed through Alembic migrations instead of relying on `Base.metadata.create_all()`.

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

The Round and Event APIs store structured gameplay data for each match session. These records power statistics, rule-based tactical analysis, and future AI coaching feedback.

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

## Match Statistics API

The Statistics API calculates match-level metrics from stored rounds and events. These statistics are used by the tactical rule engine.

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

* Total rounds
* Rounds won and lost
* Attack and defense round counts
* Attack, defense, and overall win rates
* Spike plants
* Post-plant losses
* Total gameplay events
* Event counts by type
* First death count
* Utility unused count
* Trade kill count

## Rule-Based Analysis API

The Rule-Based Analysis API converts stored rounds, events, and match statistics into explainable tactical findings. This is the first analysis layer before adding LLM-generated coaching summaries.

### Analyze Match

```http
POST /matches/{match_id}/analyze
```

This endpoint generates rule-based findings and saves them to the `analysis_findings` table.

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

### Rules Currently Implemented

* Repeated first deaths
* Post-plant conversion issues
* Utility unused in lost rounds
* Low trade support
* Low round conversion

### Why This Layer Exists

The rule engine creates evidence-based findings before the LLM layer is added. This reduces hallucination risk because future AI coaching summaries can be grounded in structured statistics and deterministic findings.

## Persisted Analysis Results API

The backend stores rule-based tactical findings in PostgreSQL so analysis results can be retrieved later by the dashboard or future LLM coaching layer.

## Coach Summary API

The Coach Summary API creates a match-level coaching explanation from saved statistics and persisted tactical findings.

The current implementation uses a deterministic mock coach. This prepares the backend structure for future LLM-generated coaching summaries while keeping the current system testable without external API calls.

## Coach Prompt API

The Coach Prompt API builds an evidence-grounded prompt from match metadata, statistics, and persisted tactical findings.

This endpoint does not call an LLM directly. It prepares the structured prompt that a future LLM client will use to generate coaching summaries.

### Get Coach Prompt

```http
GET /matches/{match_id}/coach-prompt
```

Example response:

```json
{
  "match_id": 1,
  "prompt_type": "evidence_grounded_coaching_prompt",
  "prompt": "You are an expert Valorant coach and esports analyst..."
}
```

The prompt includes:

- Match context
- Match statistics
- Tactical findings
- Output requirements
- Anti-hallucination instructions
- Confidence and limitation instructions

### Why This Layer Exists

The prompt builder separates evidence preparation from LLM execution. This keeps the future LLM layer grounded, testable, and easier to debug.

### Generate and Save Coach Summary

```http
POST /matches/{match_id}/coach-summary
```

This endpoint uses saved analysis findings and match statistics to generate a coaching summary and save it to PostgreSQL.

### Get Saved Coach Summary

```http
GET /matches/{match_id}/coach-summary
```

Example response:

```json
{
  "id": 1,
  "match_id": 1,
  "overall_summary": "This match contains 4 tactical findings across 3 tracked rounds. The overall round win rate was 0.33...",
  "primary_issue": "post_plant_conversion_issue",
  "key_evidence": "Round 2 has spike_planted=true and round_result=lost.",
  "practice_recommendation": "Review post-plant positioning, crossfire setup, utility usage, and whether players over-peeked instead of playing time.",
  "source": "mock_coach",
  "created_at": "2026-06-01T...",
  "updated_at": "2026-06-01T..."
}
```

### Why This Layer Exists

This layer converts structured statistics and rule-based findings into a human-readable coaching summary. The current mock coach keeps the system deterministic and testable. A future LLM layer can replace the mock generator while still grounding output in saved evidence.

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

## Validation Rules

The backend validates structured gameplay data before saving it to PostgreSQL.

Current validation includes:

* Round side must be `attack` or `defense`
* Round result must be `won` or `lost`
* Event type must be one of the supported tactical event types
* Confidence must be between `0.0` and `1.0`
* Round number must be between `1` and `30`
* Round end time cannot be earlier than round start time

Invalid values return a `422 Unprocessable Entity` response.

## Testing

The backend uses `pytest` and FastAPI `TestClient` for automated API testing.

Run tests from the `backend/` folder:

```bash
pytest
```

Current tests cover:

* Root endpoint
* Health endpoint
* Match creation
* Round creation
* Event creation
* Statistics calculation
* Rule-based analysis generation
* Saved analysis retrieval
* 404 handling for missing matches
* Validation tests for invalid round sides and event types
* Coach summary generation and retrieval

## Development Notes

The current MVP still includes a development/test `init_db()` helper for creating tables automatically in local and test environments. Production-style schema changes should be managed through Alembic migrations.

The current event input is manual/structured. This is intentional for the MVP because it creates reliable data for the future rule-based tactical analysis engine before adding video-processing automation.

## Database Stack

* PostgreSQL
* SQLAlchemy
* psycopg
* Redis
* Docker Compose
* Alembic