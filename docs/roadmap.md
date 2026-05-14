# Valorant AI VOD Coach Roadmap

## Product Vision

Build an AI-powered gameplay analysis platform that helps Valorant players and teams convert gameplay footage and match data into structured tactical coaching feedback.

The long-term vision is to support VOD upload, event extraction, round-level reasoning, mistake classification, personalized improvement plans, and eventually advanced video-based analysis.

---

## Phase 0: Repository and Project Foundation

Goal: Set up the project like a real production software product.

Tasks:

- Create GitHub repository
- Set up base folder structure
- Add README.md
- Add .gitignore
- Add .env.example
- Add docker-compose.yml
- Add initial documentation
- Make first Git commit

Status: In progress

---

## Phase 1: Backend API Foundation

Goal: Build the first working backend service.

Planned tasks:

- Set up FastAPI project structure
- Add health check endpoint
- Add basic configuration management
- Add local development environment
- Add backend Dockerfile
- Add API versioning structure
- Add logging setup

Expected output:

- Backend runs locally
- `/health` endpoint returns service status
- Backend can be started through Docker

---

## Phase 2: Data Model and Database

Goal: Design the first database schema for matches, rounds, players, and coaching feedback.

Planned tasks:

- Add PostgreSQL integration
- Set up SQLAlchemy or SQLModel
- Create database models
- Add Alembic migrations
- Design initial schema for:
  - matches
  - rounds
  - players
  - events
  - coaching feedback
  - processing jobs

Expected output:

- Backend can connect to PostgreSQL
- Tables can be created through migrations
- Sample match metadata can be stored and retrieved

---

## Phase 3: Match Data Ingestion

Goal: Allow the system to accept sample match data before full video processing.

Planned tasks:

- Create sample JSON match format
- Add upload endpoint for match data
- Validate uploaded data
- Store match and round data in database
- Add basic retrieval endpoints

Expected output:

- User can upload sample structured match data
- Backend stores match information
- API can return match summaries and round details

---

## Phase 4: AI Coaching Feedback MVP

Goal: Generate useful round-level coaching feedback from structured match data.

Planned tasks:

- Design coaching prompt templates
- Add AI service module
- Generate round-by-round feedback
- Classify mistakes by category
- Store AI output in database
- Add evaluation checklist for feedback quality

Mistake categories:

- Positioning
- Utility usage
- Economy decisions
- Team coordination
- Timing
- Objective control
- Death analysis

Expected output:

- System generates readable coaching feedback for each round
- Feedback is stored and retrievable through API

---

## Phase 5: Frontend MVP

Goal: Build a simple interface for viewing match analysis.

Planned tasks:

- Set up React or Next.js frontend
- Create dashboard layout
- Add match upload page
- Add match summary page
- Add round-by-round review page
- Display coaching feedback and mistake categories

Expected output:

- User can upload data through UI
- User can view match analysis results
- Project feels like an actual product demo

---

## Phase 6: Async Processing Pipeline

Goal: Move AI analysis into a background processing workflow.

Planned tasks:

- Add Redis
- Add Celery or RQ
- Create processing job model
- Add job status tracking
- Process uploads asynchronously
- Add frontend polling for job completion

Expected output:

- Upload creates a background job
- Backend tracks processing status
- AI feedback is generated asynchronously

---

## Phase 7: Video Processing Prototype

Goal: Begin extracting useful signals from VOD files.

Planned tasks:

- Define supported video input format
- Add video upload endpoint
- Extract metadata from video files
- Sample frames from gameplay
- Explore OCR for HUD information
- Explore minimap and kill feed detection

Expected output:

- Backend can accept VOD uploads
- System can extract basic video metadata
- Initial computer vision research is documented

---

## Phase 8: Deployment and Production Readiness

Goal: Prepare the project for portfolio and employer review.

Planned tasks:

- Add Dockerfiles
- Add deployment documentation
- Add GitHub Actions CI
- Add tests
- Add linting and formatting
- Add API documentation screenshots
- Add architecture diagram
- Add demo video or GIF

Expected output:

- Project can be run by another developer
- GitHub repo looks professional
- README clearly communicates technical depth

---

## Hiring Value

This project is intended to demonstrate skills relevant to:

- AI Engineer
- Machine Learning Engineer
- Applied AI Engineer
- Analytics Engineer
- Backend Engineer
- Graduate Software Engineer

Key skills demonstrated:

- Product-oriented AI system design
- Backend API development
- Database schema design
- LLM integration
- Async processing
- Docker-based development
- Technical documentation
- Computer vision exploration
- Real-world software architecture