# DATA SCHEMA

## 1. sessions
*Tracks the simulated active multiplayer sessions.*
- `session_id` (String): Unique identifier.
- `player_count` (Integer): Current number of connected players.
- `version` (Integer): Monotonically increasing state version.
- `state` (JSON): The current payload (scores, inventory, positions).
- `updated_at` (Timestamp): Last modification time.

## 2. backups
*Metadata about successful backup snapshots.*
- `backup_id` (String): Unique identifier for the backup.
- `created_at` (Timestamp): When the backup was completed.
- `source_session_version` (Integer): The session version this backup represents.
- `size_bytes` (Integer): Payload size.
- `checksum` (String): SHA-256 hash.
- `status` (String): e.g., "COMPLETED", "FAILED"

## 3. restore_attempts
*Logs of execution for the restore engine.*
- `attempt_id` (String): Unique attempt ID.
- `backup_id` (String): Foreign key to the backup being tested.
- `started_at` (Timestamp): Drill start time.
- `completed_at` (Timestamp): Drill completion time.
- `recovery_time_seconds` (Float): Total duration.
- `status` (String): "SUCCESS", "ERROR".
- `error_message` (String): Details if status is ERROR.

## 4. validation_results
*Integrity checks for the restored data.*
- `validation_id` (String): Unique ID.
- `attempt_id` (String): Foreign key to the restore attempt.
- `checksum_match` (Boolean): True if SHA-256 matches.
- `record_count_match` (Boolean): True if event count matches expected.
- `state_match` (Boolean): True if final reconstructed JSON matches.
- `corrupted_records` (Integer): Count of unreadable/modified records.
- `validation_status` (String): "PASS", "FAIL".

## 5. drill_results
*Final aggregated report metrics.*
- `drill_id` (String): Unique Drill ID.
- `attempt_id` (String): Foreign key to the restore attempt.
- `rto_target` (Integer): Target in seconds (e.g., 60).
- `rpo_target` (Integer): Target in seconds (e.g., 30).
- `actual_rto` (Float): Measured recovery time.
- `actual_rpo` (Float): Measured data age.
- `rto_pass` (Boolean): True if actual <= target.
- `rpo_pass` (Boolean): True if actual <= target.
- `overall_result` (String): "PASS" or "FAIL".
- `recommendation` (String): Human-readable advice.
