# Demo Workflow

This document explains how to test the current backend workflow for the Valorant AI VOD Coach project.

The current backend supports:

```text
Match → Round → Event → Statistics → Rule-Based Analysis → Persisted Findings
```

## Prerequisites

Start PostgreSQL and Redis:

```bash
docker compose up -d db redis
```

Run the backend from the `backend/` folder:

```bash
python -m uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Step 1: Create a Match

Endpoint:

```http
POST /matches
```

Use:

```json
{
  "title": "Sample Ascent Ranked VOD Review",
  "map_name": "Ascent",
  "player_agent": "Jett",
  "rank": "Gold 2"
}
```

Save the returned `id`.

Example:

```text
match_id = 1
```

## Step 2: Create Rounds

Endpoint:

```http
POST /matches/{match_id}/rounds
```

Create these rounds one by one.

Round 1:

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

Round 2:

```json
{
  "round_number": 2,
  "side": "attack",
  "round_result": "lost",
  "spike_planted": true,
  "site": "A",
  "start_time_seconds": 96,
  "end_time_seconds": 190
}
```

Round 3:

```json
{
  "round_number": 3,
  "side": "defense",
  "round_result": "won",
  "spike_planted": false,
  "site": null,
  "start_time_seconds": 191,
  "end_time_seconds": 280
}
```

Save the returned round IDs.

Example:

```text
round_1_id = 1
round_2_id = 2
round_3_id = 3
```

## Step 3: Create Gameplay Events

Endpoint:

```http
POST /rounds/{round_id}/events
```

Event 1 — first death in round 1:

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

Event 2 — first death in round 2:

```json
{
  "timestamp_seconds": 30,
  "event_type": "first_death",
  "actor": "self",
  "target": null,
  "location": "A main",
  "description": "Player died first while entering A main.",
  "source": "manual",
  "confidence": 1.0
}
```

Event 3 — utility unused in round 2:

```json
{
  "timestamp_seconds": 74,
  "event_type": "utility_unused",
  "actor": "self",
  "target": null,
  "location": "A site",
  "description": "Player died after spike plant with dash and smoke still available.",
  "source": "manual",
  "confidence": 1.0
}
```

Event 4 — trade kill in round 3:

```json
{
  "timestamp_seconds": 44,
  "event_type": "trade_kill",
  "actor": "teammate",
  "target": "enemy",
  "location": "B main",
  "description": "Teammate traded the first contact quickly.",
  "source": "manual",
  "confidence": 1.0
}
```

## Step 4: Get Match Statistics

Endpoint:

```http
GET /matches/{match_id}/statistics
```

Expected result includes:

```json
{
  "total_rounds": 3,
  "rounds_won": 1,
  "rounds_lost": 2,
  "spike_plants": 1,
  "post_plant_losses": 1,
  "first_death_count": 2,
  "utility_unused_count": 1,
  "trade_kill_count": 1
}
```

## Step 5: Run and Save Analysis

Endpoint:

```http
POST /matches/{match_id}/analyze
```

This generates rule-based findings and saves them to PostgreSQL.

Expected findings may include:

- early round risk
- post-plant conversion issue
- utility unused in lost round
- possible trade support gap

## Step 6: Retrieve Saved Analysis

Endpoint:

```http
GET /matches/{match_id}/analysis
```

This returns saved tactical findings from PostgreSQL.

## Current System Limitation

The current system uses manually entered structured events. Video-based event extraction will be added later.

Current flow:

```text
Manual Events → Statistics → Rule Engine → Saved Findings
```

Future flow:

```text
Video Upload → Event Extraction → Statistics → Rule Engine → LLM Coaching
```