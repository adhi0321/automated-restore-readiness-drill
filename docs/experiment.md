# EXPERIMENT METHODOLOGY

## Setup
The experiment involves generating 10 simulated multiplayer backups to evaluate the restore-readiness engine's capability to detect both healthy and corrupted states.

## Dataset Composition (10 Drills)
1. **6x Normal Backups:** Standard, healthy data snapshots. Should result in PASS.
2. **1x Corrupted Backup:** The payload is modified (bit rot / tampering) after creation, breaking the SHA-256 checksum.
3. **1x Duplicate-Event Scenario:** The backup contains identically ID'd events. The engine must deduplicate them to maintain state validity.
4. **1x Out-of-Order Scenario:** Events are stored with non-sequential timestamps. The engine must sort and apply them by correct versioning to achieve state match.
5. **1x Delayed-Event Scenario:** Simulates a straggler event. The engine should process it securely without breaking subsequent states.

## Execution
Run `python run_demo.py` to:
1. Generate the simulated dataset.
2. Inject the specific failure modes.
3. Run the restore drill engine over all 10 candidates.
4. Collect RTO/RPO and validation metrics.
5. Output the results to the SQLite metadata database for dashboard rendering.
