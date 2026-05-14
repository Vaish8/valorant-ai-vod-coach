# Valorant AI VOD Coach

## Project Overview

Valorant AI VOD Coach is a production-oriented AI/ML software project that analyzes Valorant gameplay videos and match data to generate round-by-round coaching feedback.

The goal is to help players identify individual mistakes, team-level tactical issues, poor decision-making patterns, and improvement opportunities using a combination of video processing, match statistics, backend engineering, and AI reasoning.

This project is being built as a deployable AI product, not a tutorial clone or academic-only prototype.

## Problem Statement

Valorant players often review gameplay manually or depend on human coaches to identify mistakes. This process is time-consuming, subjective, and difficult to scale.

Most players struggle to consistently answer questions such as:

- Why did we lose this round?
- Was the mistake mechanical, tactical, positional, or team-related?
- Did I use utility correctly?
- Was my death avoidable?
- What should I improve before the next match?

Valorant AI VOD Coach aims to convert gameplay footage and structured match data into actionable coaching insights.

## Target Users

The initial target users are:

- Valorant players who want structured VOD review
- Competitive players trying to improve decision-making
- Amateur teams reviewing round-level mistakes
- Coaches who want faster analysis workflows
- Esports analysts interested in AI-assisted review tools

## MVP Scope

The MVP will focus on a narrow but valuable version of the product.

### MVP Features

- Upload a gameplay VOD or sample match data
- Store match metadata and round information
- Extract basic round-level events
- Generate AI-assisted coaching feedback per round
- Categorize mistakes into tactical, positioning, utility, economy, and team coordination issues
- Display analysis results through a simple web interface

### Out of Scope for MVP

The following features are intentionally excluded from the first version:

- Real-time gameplay coaching
- Fully automated computer vision for every in-game event
- Advanced minimap tracking
- Agent-specific deep strategy engine
- Team voice communication analysis
- Ranked matchmaking integration

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