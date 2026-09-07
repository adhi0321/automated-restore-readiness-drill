# AUTOMATED RESTORE-READINESS DRILL

## Project Overview
This project simulates an automated restore-readiness engine for a multiplayer session-state system. While backups frequently complete successfully (status 200 OK), their ability to be correctly restored is rarely verified. This project establishes an automated drill engine that continuously tests backup viability against RTO and RPO targets.

## Problem Statement
Multiplayer session state changes rapidly. A corrupted backup, duplicate events, or delayed event processing can break game state consistency upon recovery.

## Objectives
- Simulate continuous session data creation.
- Generate backups and logs automatically.
- Automate restore drills to a safe, isolated testing boundary.
- Validate checksums, data integrity, and recovery SLA limits (RTO/RPO).
- Prove that the system can deduplicate and reorder events gracefully without corrupting state.

## Technology Stack
- **Backend:** Python, FastAPI
- **Database:** SQLite
- **Frontend:** HTML, CSS, JS
- **Testing:** Pytest
- **Containerization:** Docker & Docker Compose

## Setup
### Local Environment
1. Ensure Python 3.9+ is installed.
2. `cd restore-readiness-drill`
3. Create venv: `python -m venv .venv`
4. Activate venv:
   - Mac/Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`

## How to Run

**1. Run the Experiment (Populate Dataset)**
```bash
python run_demo.py
```
This generates the simulated backups, injects failure cases (corruptions, duplicate events, out-of-order data), and runs 10 restore attempts, saving the metrics to SQLite.

**2. Start the Backend Dashboard**
```bash
uvicorn backend.main:app --reload --port 8000
```
Open your browser to `http://localhost:8000/`.

**3. Run Automated Tests**
```bash
pytest
```

## Example Results
You will see that the normal backups pass state matching and checksum validation.
The duplicated and out-of-order event backups will PASS because the engine successfully deduplicates by `event_id` and reorders by `version`.
The corrupted backup will FAIL because the SHA-256 validation prevents data rot from entering the restored state.

## Limitations & Future Improvements
- **Current (First 35%):** Uses SQLite and basic memory-state reconstruction.
- **Future Stages:** Extend to use real cloud data stores (e.g., PostgreSQL, Redis), parallelize restore jobs, and implement full RBAC.
