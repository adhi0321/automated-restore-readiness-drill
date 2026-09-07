# USER FLOW

## Steps

1. **User opens dashboard:** The user accesses `http://localhost:8000/` to view the web dashboard.
2. **User selects restore drill:** The user clicks the "Run Drill Experiment" button.
3. **System loads backup candidates:** The backend fetches a list of available mock backups from the SQLite metadata store.
4. **System checks backup age:** The engine determines the creation time to evaluate the RPO metric.
5. **System creates isolated restore environment:** A temporary SQLite table or in-memory dictionary is initialized to prevent production contamination.
6. **System attempts restore:** The backup JSON is parsed and events are replayed/loaded into the isolated environment.
7. **System calculates checksum:** SHA-256 is run on the restored data payload and compared to the backup log's checksum.
8. **System validates restored session state:** The engine checks for duplicate prevention, out-of-order resolution, and record completeness.
9. **System measures recovery duration:** `end_time - start_time` is recorded.
10. **System checks RTO:** Compared against the 60-second target.
11. **System checks RPO:** Compared against the 30-second target (simulated).
12. **System records success/failure:** The Drill Result is written to the SQLite database.
13. **System gives simple recommendation:** A human-readable recommendation is generated (e.g., "Validation failed due to data corruption. Investigate backup storage integrity.")
