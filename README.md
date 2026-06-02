# Valorant AI VOD Coach

![Backend CI](https://github.com/Vaish8/valorant-ai-vod-coach/actions/workflows/backend-ci.yml/badge.svg)

## Project Overview

Valorant AI VOD Coach is a production-oriented AI/ML software project that analyzes Valorant gameplay data and structured match events to generate tactical coaching feedback.

The goal is to help players identify individual mistakes, team-level tactical issues, poor decision-making patterns, and improvement opportunities using a combination of structured gameplay events, match statistics, backend engineering, rule-based analysis, and LLM-ready coaching workflows.

This project is being built as a deployable AI product, not a tutorial clone or academic-only prototype.

## Problem Statement

Valorant players often review gameplay manually or depend on human coaches to identify mistakes. This process is time-consuming, subjective, and difficult to scale.

Most players struggle to consistently answer questions such as:

* Why did we lose this round?
* Was the mistake mechanical, tactical, positional, or team-related?
* Did I use utility correctly?
* Was my death avoidable?
* What should I improve before the next match?

Valorant AI VOD Coach aims to convert gameplay footage and structured match data into actionable coaching insights.

## Target Users

The initial target users are:

* Valorant players who want structured VOD review
* Competitive players trying to improve decision-making
* Amateur teams reviewing round-level mistakes
* Coaches who want faster analysis workflows
* Esports analysts interested in AI-assisted review tools

## MVP Scope

The MVP focuses on a narrow but valuable version of the product.

### MVP Features

* Store match metadata and round information
* Store structured gameplay events
* Calculate match-level statistics from round and event data
* Build rule-based tactical analysis over match events
* Persist tactical findings in PostgreSQL
* Generate match-level coaching summaries from saved findings
* Build evidence-grounded prompts for future LLM coaching
* Generate mock LLM coaching responses through a provider-agnostic client abstraction
* Prepare the backend for future video upload, video processing, and frontend dashboard layers

### Out of Scope for Current MVP

The following features are intentionally excluded from the current backend-first MVP:

* Real-time gameplay coaching
* Fully automated computer vision for every in-game event
* Advanced minimap tracking
* Agent-specific deep strategy engine
* Team voice communication analysis
* Ranked matchmaking integration
* Production frontend dashboard
* Full video-to-event extraction pipeline

These may be considered for later versions after the core backend and coaching workflow are stable.

## Planned Architecture

The planned system architecture is:

```text
Frontend 
   |
   v
Backend API
   |
   v
Job Queue / Async Processing
   |
   v
AI Analysis Service
   |
   v
Database + File Storage
```

## Current Backend Data Flow

The backend currently supports the following structured workflow:

```text
Match Session
   |
   v
Rounds
   |
   v
Gameplay Events
   |
   v
Statistics
   |
   v
Rule-Based Tactical Analysis
   |
   v
Persisted Findings
   |
   v
Coach Summary
   |
   v
Evidence-Grounded Coach Prompt
   |
   v
Mock LLM Coaching Response
```

## Implementation Phases

### Phase 1: Backend Foundation

Implemented the core backend foundation required for a production-style API service.

Key work completed:

* Initialized project repository structure
* Added FastAPI backend skeleton
* Added root and health check endpoints
* Added environment-based configuration
* Added CORS middleware for frontend integration
* Added automatic API documentation through Swagger UI
* Added PostgreSQL and Redis services using Docker Compose
* Configured SQLAlchemy database engine and session management
* Added database health check endpoint at `/db/health`

### Phase 2: Structured Gameplay Data Pipeline

Built the core data model for representing Valorant VOD review sessions using match, round, and gameplay event entities.

Key work completed:

* Added `Match` database model for Valorant VOD review sessions
* Added match creation and retrieval APIs
* Added `Round` and `Event` database models for structured VOD analysis
* Added APIs for creating and retrieving rounds and events
* Added service-layer functions for database operations
* Added Pydantic schemas for request and response validation
* Built the `Match → Round → Event` foundation for future tactical analysis

Current data relationship:

```text
Match
   |
   v
Round
   |
   v
Event
```

### Phase 3: Statistics and Rule-Based Tactical Analysis

Added the first analysis layer by calculating match-level statistics and applying deterministic rules to generate explainable tactical findings.

Key work completed:

* Added match statistics service
* Added `GET /matches/{match_id}/statistics` endpoint
* Calculated round, side, spike, and event-based metrics
* Calculated tactical signals such as `first_death`, `utility_unused`, and `trade_kill`
* Added rule-based tactical analysis engine
* Added `POST /matches/{match_id}/analyze` endpoint
* Implemented rules for repeated first deaths, post-plant conversion issues, utility unused in lost rounds, low trade support, and low round conversion
* Added database persistence for tactical findings
* Added `GET /matches/{match_id}/analysis` endpoint for retrieving saved analysis results

Analysis flow:

```text
Rounds + Events
      |
      v
Statistics
      |
      v
Rule-Based Findings
      |
      v
Persisted Analysis Results
```

### Phase 4: Coaching Summary and LLM-Ready Architecture

Added the first AI-product layer by converting saved statistics and tactical findings into coaching summaries, evidence-grounded prompts, and mock LLM coaching responses.

Key work completed:

* Added `CoachSummary` database model for storing match-level coaching summaries
* Added `POST /matches/{match_id}/coach-summary` endpoint
* Added `GET /matches/{match_id}/coach-summary` endpoint
* Added evidence-grounded coach prompt builder
* Added `GET /matches/{match_id}/coach-prompt` endpoint
* Added anti-hallucination instructions and structured output requirements for future LLM coaching
* Added provider-agnostic LLM client abstraction
* Added mock LLM client for deterministic local and CI-safe testing
* Added `POST /matches/{match_id}/llm-coaching` endpoint
* Added environment-based LLM configuration using `LLM_PROVIDER`, `LLM_MODEL`, and `OPENAI_API_KEY`

LLM-ready flow:

```text
Match Metadata
+ Statistics
+ Saved Tactical Findings
        |
        v
Coach Prompt
        |
        v
LLM Client
        |
        v
Coaching Response
```

### Phase 5: Backend Quality and Production Readiness

Improved backend reliability, maintainability, testing, and production readiness.

Key work completed:

* Added enum-based validation for round sides, round results, and gameplay event types
* Added timestamp validation to prevent invalid round time ranges
* Migrated settings configuration to Pydantic v2 `SettingsConfigDict`
* Added automated backend tests using `pytest` and FastAPI `TestClient`
* Tested the full Match → Round → Event → Statistics → Analysis → Coaching workflow
* Added validation tests for invalid round sides and event types
* Added GitHub Actions workflow for automated backend testing
* Configured CI to run on pushes and pull requests to `main`
* Added PostgreSQL and Redis service containers for CI test execution
* Added Alembic for version-controlled PostgreSQL database migrations
* Generated initial database schema migration for `matches`, `rounds`, `events`, and `analysis_findings`
* Generated additional migration for `coach_summaries`
* Documented migration commands for creating, applying, and checking schema versions

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* PostgreSQL
* Redis
* Docker Compose
* Uvicorn
* Alembic
* pytest
* GitHub Actions
* LLM client abstraction

### Planned Frontend

* React or Next.js
* Tailwind CSS
* Dashboard UI for match, round, event, statistics, analysis, and coaching results

### Planned AI/ML Layer

* Rule-based tactical analysis
* Evidence-grounded LLM coaching summaries
* Video metadata extraction
* Future OpenCV-based event extraction

## Current Status

The project currently has a working backend foundation with:

* API health check
* Database health check
* PostgreSQL connection
* Match session creation and retrieval
* Round creation and retrieval
* Gameplay event creation and retrieval
* Match statistics calculation from structured round and event data
* Rule-based tactical analysis from structured match statistics and events
* Persistent analysis findings stored in PostgreSQL
* Coach summary generation from saved statistics and tactical findings
* Evidence-grounded coach prompt generation for future LLM summaries
* Mock LLM coaching generation through a provider-agnostic client abstraction
* Sample demo workflow and JSON payloads for testing the backend analysis pipeline
* Automated backend tests for the core analysis and coaching workflow
* Enum-based validation for structured round and event data
* GitHub Actions CI for automated backend testing
* Alembic database migrations for version-controlled schema management

## API Capabilities

Current backend endpoints support:

* Match session creation and retrieval
* Round creation and retrieval
* Gameplay event creation and retrieval
* Match statistics calculation
* Rule-based tactical analysis generation
* Saved analysis retrieval
* Coach summary generation and retrieval
* Evidence-grounded coach prompt generation
* Mock LLM coaching response generation
* Health and database health checks

Swagger API docs are available locally at:

```text
http://127.0.0.1:8000/docs
```

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

## Testing and CI

The backend uses automated tests to validate the core workflow.

Current tests cover:

* Root endpoint
* Health endpoint
* Match creation
* Round creation
* Event creation
* Statistics calculation
* Rule-based analysis generation
* Saved analysis retrieval
* Validation failures for invalid gameplay inputs
* Coach summary generation and retrieval
* Coach prompt generation
* Mock LLM coaching response generation

GitHub Actions runs the backend test suite automatically on pushes and pull requests to `main`.

## Current Limitations

The current MVP uses manually entered structured events. This is intentional because it creates reliable evidence for statistics, rule-based analysis, prompt generation, and mock LLM coaching before attempting harder video-based event extraction.

Current limitations:

* No production frontend yet
* No real video upload or video processing pipeline yet
* No automated computer vision event extraction yet
* LLM coaching currently uses a mock provider by default
* No user authentication or multi-user workspace yet
* No deployed production environment yet

## Next Planned Milestone

The next planned milestone is to add optional real LLM provider integration while keeping mock mode as the default for local development and CI.

Planned next work:

```text
Add optional OpenAI client integration behind the existing LLM provider abstraction.
```

## Notes

This project is under active development. The current focus is building a reliable backend and structured data pipeline before adding advanced video processing, frontend dashboard features, or production deployment.

The current backend deliberately separates statistics, rule-based analysis, prompt building, and LLM generation. This makes the system easier to test, easier to debug, and safer against hallucinated coaching output.
