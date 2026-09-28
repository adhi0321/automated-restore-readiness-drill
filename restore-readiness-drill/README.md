# AUTOMATED RESTORE-READINESS DRILL (70% MILESTONE)
### For Multiplayer Session-State Systems

## Project Overview
This project delivers an automated **Restore-Readiness Drill** engine for high-velocity multiplayer session-state systems. While backups frequently report success (`200 OK`), their real-world restorability is rarely tested until an actual disaster occurs. This system continuously runs automated restore drills in isolated sandboxes to verify data integrity, cryptographic SHA-256 consistency, and strict SLA compliance against **Recovery Time Objective (RTO ≤ 60s)** and **Recovery Point Objective (RPO ≤ 30s)**.

---

## 70% Milestone Deliverables Completed
1. **Full Backend Architecture:** Clean separation of concerns with FastAPI service layer, SQLite persistence engine, simulation harnesses, validation engines, and chaos failure injectors.
2. **Persistent SQLite Database:** Structured schema recording drill executions, start/completion timestamps, checksum outcomes, state fidelity, actual vs target RTO/RPO, and actionable recommendations.
3. **End-to-End Automated Workflow:** Automated snapshot generation, SHA-256 calculation, failure injection, sandbox restoration, state reconstruction, and telemetry storage.
4. **Expanded 9-Scenario Chaos Testing System:**
   - `NORMAL`: Healthy baseline state snapshot.
   - `CORRUPT_CHECKSUM`: Simulates bit rot; fails checksum validation immediately.
   - `DUPLICATE_EVENT`: Tests idempotency; duplicate events are discarded without duplicating score/items.
   - `OUT_OF_ORDER`: Tests Lamport version ordering; out-of-order sequence packets are safely reordered.
   - `DELAYED_STRAGGLER`: Tests late arrival packet processing without corrupting the active world sequence.
   - `TRUNCATED_WAL`: Simulates sudden node termination during write log flushing.
   - `RTO_BREACH`: Simulates slow I/O exceeding the 60s RTO objective.
   - `RPO_BREACH`: Simulates overdue backup schedules exceeding the 30s RPO limit.
   - `CONCURRENT_CONFLICT`: Tests simultaneous conflicting mutations on contested game resources.
5. **Zero-Dependency Python Execution:** Runs out-of-the-box on standard Python 3.9+ with built-in `dataclasses` and `sqlite3`, with automatic full integration with `pydantic` and `fastapi` when installed.
6. **Automated Test Suite:** 11 comprehensive automated tests runnable via `python3 -m unittest discover tests` or `pytest`.
7. **REST API Endpoints:** Rich endpoints for running drills, batch experiments, retrieving metrics, risk registers, and exportable audit reports.
8. **Comprehensive Stakeholder & Executive Documentation:** Located in `docs/` covering architecture, benchmarks, risk registers, and stakeholder briefings.

---

## Technology Stack
- **Backend:** Python 3.9+, FastAPI, SQLite 3
- **Testing:** Pytest / Python standard `unittest`
- **Frontend & UI:** High-Density interactive web interface (Next.js & pure static HTML/JS)
- **Containerization:** Docker & Docker Compose

---

## Quickstart & Local Execution

### 1. Run Automated Tests
```bash
cd restore-readiness-drill
PYTHONPATH=. python3 -m unittest discover tests
# Or using pytest:
pytest tests/
```
All 11 tests will execute and validate backup creation, restore reconstruction, RTO/RPO calculation, failure modes, and database persistence.

### 2. Run the Demo Experiment
```bash
PYTHONPATH=. python3 run_demo.py
```
This script initializes the SQLite database, simulates 100 multiplayer tick events, creates backups, executes 10 restore drills across multiple failure modes, records results, and exports `data/sample_backup.json`.

### 3. Start the FastAPI Service
```bash
uvicorn backend.main:app --reload --port 8000
```
Then navigate to `http://localhost:8000/` for the web dashboard.

---

## REST API Specification

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/results` | Returns all recorded drill results from the SQLite database. |
| `GET` | `/api/metrics` | Returns executive recovery rates, MTTR, RTO/RPO compliance %, and failure breakdowns. |
| `POST` | `/api/drills/run?scenario={SCENARIO}` | Executes an automated drill against the specified failure scenario. |
| `POST` | `/api/experiments/batch?count=10` | Runs a multi-iteration batch experiment across mixed scenarios. |
| `GET` | `/api/risk-register` | Returns the disaster recovery risk register with likelihood and mitigations. |
| `GET` | `/api/baseline-comparison` | Returns structured comparison of traditional backups vs automated drills. |
| `GET` | `/api/report/export` | Generates an exportable JSON and Markdown technical audit report. |

---

## Documentation Index
- `docs/architecture.md`: Full architectural blueprint and pipeline flow.
- `docs/baseline.md`: Side-by-side comparison of baseline vs prototype.
- `docs/benchmarks.md`: Performance and recovery speed benchmarks.
- `docs/data_schema.md`: Detailed SQLite table definitions and event payload formats.
- `docs/experiment.md`: Experiment setup, failure injection methodology, and success criteria.
- `docs/risk_register.md`: Disaster recovery risk register and mitigation matrix.
- `docs/stakeholder_validation.md`: Non-specialist executive briefing on why backup success is deceptive.
- `docs/user_guide.md`: Step-by-step setup and operational user manual.

