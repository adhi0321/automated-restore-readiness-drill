# AUTOMATED RESTORE-READINESS DRILL: COMPLETE USER GUIDE

Welcome to the **Automated Restore-Readiness Drill** platform. This guide is written for beginner operators, student reviewers, and studio leads. It guides you step-by-step through installing, running drills, executing chaos scenarios, reading metrics, and reproducing the 30-drill controlled experiment.

---

## 1. Quick Introduction
A backup finishing successfully does not prove that your game can be recovered. This system automatically tests your backups in an isolated test environment to prove whether they can actually be restored without losing player progress or violating recovery deadlines.

---

## 2. System Requirements
- **Operating System:** Windows, macOS, or Linux.
- **Python:** Python 3.9 or higher (standard library only; no external pip dependencies strictly required).
- **Node.js (Optional, for web frontend):** Node.js 18+ and npm if running the Next.js preview locally.

---

## 3. Installation and Setup

### Method A: Zero-Dependency Python Execution
1. Open a terminal in the project directory.
2. Verify Python is installed:
   ```bash
   python3 --version
   ```
3. Run the automated test suite directly:
   ```bash
   python3 run_all_tests.py
   ```
   *(All 13 tests will run and pass using Python's standard library).*

### Method B: Setting up Python Virtual Environment (Optional)
If you wish to use FastAPI and Uvicorn for local web hosting:
```bash
cd restore-readiness-drill
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Starting the Application

### Option A: Viewing the Interactive Web Dashboard (Next.js)
If developing locally:
```bash
npm install
npm run dev
```
Open your browser to: `http://localhost:3000/`.  
*(In Google AI Studio Preview, this renders automatically at `/` on port 3000).*

### Option B: Starting the Python FastAPI Backend
```bash
cd restore-readiness-drill
uvicorn backend.main:app --reload --port 8000
```
Open your browser to: `http://localhost:8000/`.

---

## 5. Running a Restore Drill
1. Open the dashboard in your browser.
2. In the top action bar, click **"Run Restore Drill"** (or **"Normal Restore"**).
3. The system will:
   - Package a simulated live multiplayer session snapshot.
   - Calculate its SHA-256 cryptographic checksum.
   - Restore the snapshot into an isolated sandbox.
   - Compare the restored player positions, health, and scores with ground truth.
   - Clock the exact recovery duration in milliseconds.
   - Display a green **PASS** indicator if all checks succeed.

---

## 6. Running Failure and Chaos Scenarios
Under the **Chaos & Failure Injection Engine** section of the dashboard, you can trigger specific failure modes with one click:
- **Corrupted Backup:** Simulates silent bit-rot. The SHA-256 checksum fails, and the restore is safely aborted.
- **Duplicate Event:** Simulates network packet retries. The deduplication filter drops duplicate packets, ensuring players don't receive double currency.
- **Out-of-Order Event:** Simulates network jitter. The engine reorders packets by version number before state application, preventing players from teleporting backwards.
- **Delayed Event:** Simulates a late-arriving packet. The Lamport version gate prevents stale packets from overwriting newer match actions.
- **Truncated WAL:** Simulates a sudden node crash mid-write. The engine halts at the last valid atomic checkpoint.
- **RTO Breach:** Simulates slow disk I/O exceeding 60s, triggering an SLA alert.
- **RPO Breach:** Simulates a stale snapshot older than 30s, triggering a data loss alert.

---

## 7. Running the 30-Drill Controlled Experiment
To reproduce the entire scientific experiment with deterministic random seed 42:
```bash
python3 run_final_experiment.py
```
This script will:
1. Reset the SQLite database for a clean run.
2. Execute 30 planned drills across all 9 scenarios.
3. Calculate final recovery rates, RTO/RPO compliance rates, and baseline comparisons.
4. Export raw audit data to the `evidence/` directory:
   - `evidence/final_results.csv`
   - `evidence/final_results.json`
   - `evidence/baseline_results.csv`
   - `evidence/prototype_results.csv`
   - `evidence/error_analysis.csv`
   - `evidence/state_integrity_results.json`
   - `evidence/metrics_summary.json`

---

## 8. How to Read Dashboard Metrics
- **RTO Target (60s):** Recovery Time Objective. The maximum allowable downtime. A drill fails RTO if recovery takes longer than 60 seconds.
- **RPO Target (30s):** Recovery Point Objective. The maximum allowable data staleness. A drill fails RPO if the backup data is older than 30 seconds when disaster occurs.
- **Successful Recovery Rate:** The percentage of drills where the backup restored successfully, checksum was valid, state was 100% matched, RTO was met, and RPO was met.
- **Baseline vs Prototype:** Compares how traditional passive backups would have behaved during a disaster versus our active restore-readiness engine.

---

## 9. Resetting Demo Data
To clear the SQLite database and start fresh:
```bash
rm -f restore-readiness-drill/drill_results.db
python3 run_final_experiment.py
```
Or in the web dashboard, click **"Reset Drills"** in the top action bar.

---

## 10. Running the Automated Test Suite
To verify that all backend services and validation gates are working correctly:
```bash
python3 run_all_tests.py
```
Expected output:
```text
Total Tests:   13
Passed:        13
Failed:        0
Skipped:       0
ALL TESTS PASSED SUCCESSFULLY! (100% PASS RATE)
```

---

## 11. Troubleshooting
If you encounter any issues:
- Check `docs/troubleshooting.md` for exact solutions to common issues (locked database, port conflicts, or browser cache).
