# Valorant AI VOD Coach

![Backend CI](https://github.com/Vaish8/valorant-ai-vod-coach/actions/workflows/backend-ci.yml/badge.svg)

## Project Overview

Valorant AI VOD Coach is a production-oriented AI/ML software project that analyzes Valorant gameplay videos and match data to generate round-by-round coaching feedback.

The goal is to help players identify individual mistakes, team-level tactical issues, poor decision-making patterns, and improvement opportunities using a combination of structured gameplay events, match statistics, backend engineering, rule-based analysis, and future AI reasoning.

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

* Upload a gameplay VOD or sample match data
* Store match metadata and round information
* Store structured gameplay events
* Calculate match-level statistics from round and event data
* Build rule-based tactical analysis over match events
* Persist tactical findings in PostgreSQL
* Generate future AI-assisted coaching feedback per round
* Categorize mistakes into tactical, positioning, utility, economy, and team coordination issues
* Display analysis results through a simple web interface

### Out of Scope for MVP

The following features are intentionally excluded from the first version:

* Real-time gameplay coaching
* Fully automated computer vision for every in-game event
* Advanced minimap tracking
* Agent-specific deep strategy engine
* Team voice communication analysis
* Ranked matchmaking integration

These may be considered for later versions after the core product workflow is working.

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
Future AI Coaching Feedback
```

## Development Progress

### Day 1

* Initialized project repository structure
* Added roadmap and documentation foundation

### Day 2

* Added FastAPI backend skeleton
* Added health check endpoint
* Added environment-based configuration
* Added automatic API documentation

### Day 3

* Added PostgreSQL and Redis services using Docker Compose
* Configured SQLAlchemy database engine and session management
* Added environment-based database configuration
* Added database health check endpoint at `/db/health`

### Day 4

* Added Match database model for Valorant VOD review sessions
* Added Pydantic schemas for match creation and response validation
* Added Match service layer for database operations
* Added Match API endpoints: `POST /matches`, `GET /matches`, and `GET /matches/{match_id}`

### Day 5

* Added Round and Event database models for structured VOD analysis
* Added Pydantic schemas for round and event validation
* Added service layer functions for creating and retrieving rounds/events
* Added API endpoints: `POST /matches/{match_id}/rounds`, `GET /matches/{match_id}/rounds`, `POST /rounds/{round_id}/events`, and `GET /rounds/{round_id}/events`
* Built the structured data foundation for future rule-based tactical analysis and AI coaching feedback

### Day 6

* Added backend learning notes to document the system built from Day 1 to Day 5
* Reviewed FastAPI request flow, SQLAlchemy models, Pydantic schemas, service layers, and database relationships
* Documented common development errors and fixes, including virtual environment issues, missing route registration, database authentication, and SQLAlchemy relationship configuration
* Created a study reference for explaining the Match → Round → Event backend workflow in interviews

### Day 7

* Added match statistics service to calculate round, side, spike, and event-based metrics
* Added statistics response schema for structured API output
* Added `GET /matches/{match_id}/statistics` endpoint
* Calculated event counts for tactical signals such as `first_death`, `utility_unused`, and `trade_kill`
* Created the foundation for the upcoming rule-based tactical analysis engine

### Day 8

* Added rule-based tactical analysis engine for structured match data
* Added analysis response schema with issue type, severity, evidence, recommendation, confidence, and optional round reference
* Added `POST /matches/{match_id}/analyze` endpoint
* Implemented rules for repeated first deaths, post-plant conversion issues, utility unused in lost rounds, low trade support, and low round conversion
* Created the first explainable analysis layer before adding LLM-based coaching

### Day 9

* Added database persistence for tactical analysis findings
* Added `AnalysisFinding` SQLAlchemy model for storing issue type, severity, evidence, recommendation, confidence, source, and optional round reference
* Updated `POST /matches/{match_id}/analyze` to generate and save findings to PostgreSQL
* Added `GET /matches/{match_id}/analysis` endpoint for retrieving saved analysis results
* Improved the backend workflow from temporary API-only analysis to persistent analysis results for future dashboard and LLM coaching features

### Day 10

* Added sample match, round, event, statistics, and analysis JSON files for backend demo testing
* Added demo workflow documentation explaining how to test the full Match → Round → Event → Statistics → Analysis pipeline
* Improved project reproducibility by providing example API inputs and expected outputs
* Documented the current manual-event workflow and future video-assisted analysis direction

### Day 11

* Added automated backend tests using `pytest` and FastAPI `TestClient`
* Tested health endpoints and full Match → Round → Event → Statistics → Analysis workflow
* Verified statistics calculation, rule-based analysis generation, and saved analysis retrieval
* Added 404 tests for missing match statistics, analysis, and saved findings
* Improved backend reliability by reducing reliance on manual Swagger testing

### Day 12

* Added enum-based validation for round sides, round results, and gameplay event types
* Added timestamp validation to prevent invalid round time ranges
* Updated services to store validated enum values consistently in PostgreSQL
* Migrated settings configuration to Pydantic v2 `SettingsConfigDict`
* Added validation tests for invalid round sides and event types
* Improved API reliability by preventing invalid tactical data from entering the analysis pipeline

### Day 13

* Added GitHub Actions workflow for automated backend testing
* Configured CI to run on pushes and pull requests to `main`
* Added PostgreSQL and Redis service containers for CI test execution
* Configured backend dependency installation and `pytest` execution in GitHub Actions
* Added backend CI badge to the project README after successful workflow execution

### Day 14

* Added Alembic for version-controlled PostgreSQL database migrations
* Configured Alembic to use SQLAlchemy model metadata for automatic migration generation
* Generated the initial database schema migration for `matches`, `rounds`, `events`, and `analysis_findings`
* Applied the initial migration to PostgreSQL using `alembic upgrade head`
* Documented migration commands for creating, applying, and checking database schema versions
* Kept the development/test `init_db()` helper while documenting Alembic as the production-ready schema management approach

### Day 15

- Added `CoachSummary` database model for storing match-level coaching summaries
- Added coach summary response schema, service layer, and API routes
- Added `POST /matches/{match_id}/coach-summary` endpoint to generate and save mock coaching summaries
- Added `GET /matches/{match_id}/coach-summary` endpoint to retrieve saved coaching summaries
- Generated an Alembic migration for the `coach_summaries` table
- Added tests for coach summary generation and retrieval
- Created the backend foundation for future LLM-assisted coaching summaries grounded in saved statistics and tactical findings

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

### Planned Frontend

* React or Next.js
* Tailwind CSS
* Dashboard UI for match, round, event, statistics, and analysis results

### Planned AI/ML Layer

* Rule-based tactical analysis
* LLM-assisted coaching summaries
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
* Sample demo workflow and JSON payloads for testing the backend analysis pipeline
* Automated backend tests for the core analysis workflow
* Enum-based validation for structured round and event data
* GitHub Actions CI for automated backend testing
* Alembic database migrations for version-controlled schema management
* Coach summary generation from saved statistics and tactical findings

Next planned milestone:

```text
Replace mock coaching generation with a prompt-builder and optional LLM client.
```

## Notes

This project is under active development. The current focus is building a reliable backend and structured data pipeline before adding advanced video processing or AI coaching features.

The current MVP uses manually entered structured events. This is intentional because it creates reliable evidence for statistics, rule-based analysis, and future LLM coaching before attempting harder video-based event extraction.
