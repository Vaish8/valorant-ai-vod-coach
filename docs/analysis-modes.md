# Analysis Modes

Valorant AI VOD Coach supports two complementary analysis modes.

## Mode 1: Structured Event Analysis

Structured Event Analysis uses match, round, and event data to generate tactical findings.

Current flow:

```text
Match
   |
   v
Round
   |
   v
Event
   |
   v
Statistics
   |
   v
Rule-Based Tactical Findings
   |
   v
Evidence-Grounded Coaching