import uuid
import time
from .models import BackupData, RestoreAttemptResult, SessionState, DrillResult
from .backup_service import generate_checksum
from .config import Config

def calculate_rpo(backup: BackupData, failure_time: float) -> float:
    if not backup.events:
        return failure_time - backup.created_at
    latest_event_time = max(e.timestamp for e in backup.events)
    return failure_time - latest_event_time

def run_drill(backup: BackupData, expected_state: SessionState, failure_time: float) -> dict:
    drill_id = str(uuid.uuid4())
    
    # 1. Validation (Checksum)
    backup_json = backup.model_dump_json(exclude={"checksum"})
    calculated_checksum = generate_checksum(backup_json)
    checksum_match = (calculated_checksum == backup.checksum)
    
    # 2. Restore Attempt
    from .restore_service import perform_restore
    restore_result = perform_restore(backup)
    
    # 3. Data Validation (State Match)
    state_match = False
    if restore_result.status == "SUCCESS" and restore_result.restored_state:
        state_match = (restore_result.restored_state.version == expected_state.version) and \
                      (restore_result.restored_state.state == expected_state.state)

    # 4. RTO & RPO Calculation
    actual_rto = restore_result.recovery_time_seconds
    actual_rpo = calculate_rpo(backup, failure_time)
    
    rto_pass = actual_rto <= Config.RTO_TARGET_SECONDS
    rpo_pass = actual_rpo <= Config.RPO_TARGET_SECONDS
    
    # Overall Result
    overall_pass = checksum_match and state_match and rto_pass and rpo_pass and restore_result.status == "SUCCESS"
    
    if not checksum_match:
        recommendation = "Backup completed successfully, but the restore test failed because the backup data was corrupted. Recommendation: Do not treat this backup as recovery-ready until a clean restore succeeds."
    elif not state_match:
        recommendation = "State reconstruction mismatch. The restored data does not represent the original active state accurately."
    elif not rto_pass:
        recommendation = f"Recovery took {actual_rto:.2f}s, exceeding the {Config.RTO_TARGET_SECONDS}s RTO target. Optimize the restore engine."
    elif not rpo_pass:
        recommendation = f"Data loss ({actual_rpo:.2f}s) exceeded the {Config.RPO_TARGET_SECONDS}s RPO target. Increase backup frequency."
    else:
        recommendation = "Restore drill passed successfully within RTO and RPO targets. Data integrity verified."
        
    return {
        "drill_id": drill_id,
        "backup_id": backup.backup_id,
        "attempt_id": restore_result.attempt_id,
        "started_at": restore_result.started_at,
        "completed_at": restore_result.completed_at,
        "recovery_time_seconds": actual_rto,
        "rto_target": Config.RTO_TARGET_SECONDS,
        "rpo_target": Config.RPO_TARGET_SECONDS,
        "actual_rto": actual_rto,
        "actual_rpo": actual_rpo,
        "rto_pass": int(rto_pass),
        "rpo_pass": int(rpo_pass),
        "checksum_match": int(checksum_match),
        "state_match": int(state_match),
        "overall_result": "PASS" if overall_pass else "FAIL",
        "recommendation": recommendation,
        "error_message": restore_result.error_message or ""
    }
