# TROUBLESHOOTING GUIDE

This guide provides exact, practical solutions for common operational issues encountered when running, developing, or evaluating the Automated Restore-Readiness Drill system.

---

## 1. Web Preview Issues

### Issue 1.1: Preview Displays "404 Not Found"
- **Cause:** The dev server was pointed to a non-root route, or Next.js App Router failed to serve `app/page.tsx` on the root `/`.
- **Exact Fix:**
  1. Verify that `app/page.tsx` exists and exports a default React component.
  2. Confirm the server is running on port 3000: `curl -I http://localhost:3000/`.
  3. Ensure no redirects are defined in `next.config.ts`.
  4. In the Google AI Studio Preview address bar, ensure the URL path ends with `/`.

### Issue 1.2: Stale Dashboard or Unresponsive Buttons
- **Cause:** Browser aggressive caching of client components or service worker registration.
- **Exact Fix:**
  1. Perform a hard refresh: Press `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac).
  2. Clear browser cache for `localhost:3000` or open in an Incognito / Private window.

---

## 2. Python Backend & Experiment Issues

### Issue 2.1: Python Command Differences (`python` vs `python3`)
- **Cause:** Some Linux/macOS environments do not symlink `python` to `python3`.
- **Exact Fix:**
  Use explicit `python3` with module path set:
  ```bash
  PYTHONPATH=restore-readiness-drill python3 run_final_experiment.py
  # Or from within restore-readiness-drill/:
  cd restore-readiness-drill && PYTHONPATH=. python3 run_final_experiment.py
  ```

### Issue 2.2: SQLite Database Locked (`sqlite3.OperationalError: database is locked`)
- **Cause:** An active background process or zombie uvicorn worker holds an uncommitted write lock on `drill_results.db`.
- **Exact Fix:**
  1. Identify and kill any orphaned python or uvicorn processes:
     ```bash
     pkill -f uvicorn || true
     pkill -f python3 || true
     ```
  2. Or delete the local database file to allow `init_db()` to recreate it cleanly:
     ```bash
     rm -f restore-readiness-drill/drill_results.db
     ```

### Issue 2.3: Port Already in Use (`OSError: [Errno 98] Address already in use: 8000`)
- **Cause:** FastAPI / Uvicorn is already running on port 8000 from a previous session.
- **Exact Fix:**
  Find the PID and terminate the process:
  ```bash
  lsof -ti :8000 | xargs kill -9
  # Alternatively, specify another port:
  uvicorn backend.main:app --port 8080 --reload
  ```

### Issue 2.4: Experiment Output Missing from `evidence/`
- **Cause:** `run_final_experiment.py` was executed from an unexpected directory, or encountered a permission error writing to disk.
- **Exact Fix:**
  Execute from workspace root:
  ```bash
  mkdir -p evidence
  python3 run_final_experiment.py
  ls -la evidence/
  ```

---

## 3. Test Suite Issues

### Issue 3.1: `pytest: command not found`
- **Cause:** `pytest` is not installed in the system global Python path.
- **Exact Fix:**
  The project is specifically architected with **Zero-Dependency Python Execution**. You can run all 13 tests using the standard Python library:
  ```bash
  python3 run_all_tests.py
  # Or:
  PYTHONPATH=restore-readiness-drill python3 -m unittest discover restore-readiness-drill/tests
  ```

### Issue 3.2: Stale Test State or Flaky Assertions
- **Cause:** Previous failed drills left lingering records in SQLite.
- **Exact Fix:**
  Run the test suite via `run_all_tests.py`, which initializes clean isolated test fixtures for each test method.
