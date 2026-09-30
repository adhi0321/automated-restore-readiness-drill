# TROUBLESHOOTING GUIDE & COMMON ISSUES

This guide provides exact, tested remedies for common operational issues encountered during local development, test execution, or web preview.

---

### 1. Google AI Studio Preview Returns 404
- **Problem:** Opening the web preview displays a `404 Not Found` error.
- **Cause:** Dev server is attempting to route to an unmounted sub-path or Vite router configuration rather than the root page.
- **Fix:** The application root `/` is served directly by Next.js `app/page.tsx` on port 3000. Ensure you access the base development URL directly. The self-contained client applet does not require any external proxy or sub-path routing.

---

### 2. SQLite Database is Locked (`sqlite3.OperationalError: database is locked`)
- **Problem:** Running tests or experiments reports `database is locked`.
- **Cause:** Another Python process or terminal session has an open write transaction on `drill_metadata.db`.
- **Fix:**
  ```bash
  # Check for hanging python processes:
  pkill -f "python3 run_"
  # Or safely remove temporary SQLite WAL locks:
  rm -f restore-readiness-drill/drill_metadata.db-wal restore-readiness-drill/drill_metadata.db-shm
  ```

---

### 3. Missing `scenario` Column (`no such column: scenario`)
- **Problem:** `sqlite3.OperationalError: table drill_results has no column named scenario`
- **Cause:** An old SQLite database file created before the schema update is still present.
- **Fix:** The `database.py` script automatically runs schema migrations on startup. You can also re-initialize cleanly by deleting the local database file:
  ```bash
  rm -f restore-readiness-drill/drill_metadata.db drill_metadata.db
  python3 -c "import sys; sys.path.insert(0, 'restore-readiness-drill'); from backend.database import init_db; init_db()"
  ```

---

### 4. `pytest: not found` or Missing Pip Dependencies
- **Problem:** Terminal outputs `sh: 1: pytest: not found` or `ModuleNotFoundError: No module named 'pydantic'`.
- **Cause:** Running in an environment without external pip dependencies installed.
- **Fix:** All models and tests feature zero-dependency fallbacks using Python's standard library. Run tests with standard `unittest`:
  ```bash
  PYTHONPATH=restore-readiness-drill python3 -m unittest discover restore-readiness-drill/tests
  # Or use our one-command test runner:
  PYTHONPATH=restore-readiness-drill python3 run_all_tests.py
  ```

---

### 5. Port 8000 or Port 3000 Already in Use (`EADDRINUSE`)
- **Problem:** Backend server fails to start with `address already in use`.
- **Fix:**
  ```bash
  # Find and terminate process on port 8000:
  lsof -ti :8000 | xargs kill -9
  # For port 3000 (Next.js):
  lsof -ti :3000 | xargs kill -9
  ```

---

### 6. Missing Experiment Evidence Output (`evidence/final_results.csv` not found)
- **Problem:** The evidence directory is empty or missing.
- **Fix:** Execute the reproducible experiment script:
  ```bash
  PYTHONPATH=restore-readiness-drill python3 run_final_experiment.py
  ```
  This creates both `/evidence` and `/restore-readiness-drill/evidence` populated with CSV, JSON, and metrics files.

---

### 7. Browser Cache Showing Stale Dashboard State
- **Problem:** UI does not reflect recent experiment runs.
- **Fix:** Perform a hard refresh in the browser (`Ctrl + Shift + R` or `Cmd + Shift + R`), or click the **"Reset Demo Data"** button on the dashboard to trigger an in-memory refresh.
