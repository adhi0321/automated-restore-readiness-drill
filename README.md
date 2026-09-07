# Automated Restore-Readiness Drill

## Project Overview
This project simulates an automated restore-readiness engine for a multiplayer session-state system. While backups frequently complete successfully (status 200 OK), their ability to be correctly restored and parsed is rarely verified. This MVP establishes an automated drill engine that continuously tests backup viability against Recovery Time Objective (RTO) and Recovery Point Objective (RPO) targets.

## Features
- **Session Simulation**: Automatically generates multiplayer session events (player records, scores, coordinates, inventories).
- **Restore Drills**: Simulates isolated restore attempts and measures recovery duration (RTO) and data age (RPO).
- **State Validation**: Reconstructs JSON state and verifies checksums to detect data corruption or mismatch.
- **Failure Injection**: 
  - *Normal Restore*: Baseline successful recovery.
  - *Corrupted Backup*: Simulates bit-rot; fails checksum validation.
  - *Duplicate Event*: Tests idempotency; duplicate events are safely ignored.
  - *Out-of-Order Event*: Tests sequence sorting; events are applied in correct chronological order.
  - *Delayed Event*: Tests straggler handling; late events are safely merged.
- **Real-time Dashboard**: A high-density, dark-mode UI for tracking drill success rates and displaying automated, plain-English recommendations.

## Technology Stack
- **Framework**: Next.js (React)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Architecture**: Self-contained Client Component SPA (Single Page Application) designed for immediate browser preview compatibility. *Note: The earlier Python/SQLite design was migrated to a Next.js SPA to eliminate 404 preview routing errors and allow for immediate zero-config demonstration.*

## Baseline vs. Prototype Comparison
| Metric | Baseline | Prototype |
|--------|----------|-----------|
| Restore completion check | Yes (manual) | Yes (automated) |
| Checksum validation | No | Yes |
| State validation | No | Yes |
| RTO / RPO measurement | No / Partial | Yes |
| Failure injection | No | Yes |
| Duplicate & Out-of-order handling | No | Yes |
| Automated Recommendations | No | Yes |

## How to Run Locally
1. Install the dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Open your browser and navigate to [http://localhost:3000](http://localhost:3000).

## Project Structure
- `app/page.tsx`: The main dashboard UI, metrics calculation, and failure simulation engine.
- `app/globals.css`: Global stylesheet containing Tailwind imports.
- `docs/`: Original planning documents and architecture drafts.
