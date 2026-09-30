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

def run_drill(backup: BackupData, expected_state: SessionState, failure_time: float, scenario: str = "NORMAL", session_id: str = "") -> dict:
    drill_id = str(uuid.uuid4())
    resolved_session_id = session_id or getattr(expected_state, "session_id", "session_1") or "session_1"
    
    # 1. Validation (Checksum)
    backup_json = backup.model_dump_json(exclude={"checksum"})
    calculated_checksum = generate_checksum(backup_json)
    checksum_match = (calculated_checksum == backup.checksum)
    
    # 2. Restore Attempt
    from .restore_service import perform_restore
    restore_result = perform_restore(backup)
    
    # 3. Data Validation (State Match & State Integrity)
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
    overall_pass = checksum_match and state_match and rto_pass and rpo_pass and (restore_result.status == "SUCCESS")
    
    error_reason = ""
    if not checksum_match:
        error_reason = "Cryptographic Checksum Mismatch (Corrupted Payload / Bit Rot)"
        recommendation = "Backup completed successfully, but the restore test failed because the backup data was corrupted. Recommendation: Do not treat this backup as recovery-ready until a clean restore succeeds."
    elif not state_match:
        error_reason = "State Reconstruction Mismatch (Data Divergence / Missing WAL events)"
        recommendation = "State reconstruction mismatch. The restored data does not represent the original active state accurately."
    elif not rto_pass:
        error_reason = f"RTO Target Exceeded ({actual_rto:.2f}s > {Config.RTO_TARGET_SECONDS}s)"
        recommendation = f"Recovery took {actual_rto:.2f}s, exceeding the {Config.RTO_TARGET_SECONDS}s RTO target. Optimize the restore engine and storage throughput."
    elif not rpo_pass:
        error_reason = f"RPO Target Exceeded ({actual_rpo:.2f}s > {Config.RPO_TARGET_SECONDS}s)"
        recommendation = f"Data loss ({actual_rpo:.2f}s) exceeded the {Config.RPO_TARGET_SECONDS}s RPO target. Increase backup checkpoint frequency."
    elif restore_result.status != "SUCCESS":
        error_reason = f"Restore Engine Exception: {restore_result.error_message}"
        recommendation = "Fatal crash during restore execution. Inspect exception logs."
    else:
        recommendation = "Restore drill passed successfully within RTO and RPO targets. Data integrity verified."
        
    return {
        "drill_id": drill_id,
        "scenario": scenario,
        "backup_id": backup.backup_id,
        "session_id": resolved_session_id,
        "attempt_id": restore_result.attempt_id,
        "start_time": restore_result.started_at,
        "end_time": restore_result.completed_at,
        "started_at": restore_result.started_at,
        "completed_at": restore_result.completed_at,
        "recovery_time": actual_rto,
        "recovery_time_seconds": actual_rto,
        "rto_target": Config.RTO_TARGET_SECONDS,
        "actual_rto": actual_rto,
        "rto_pass": int(rto_pass),
        "rpo_target": Config.RPO_TARGET_SECONDS,
        "actual_rpo": actual_rpo,
        "rpo_pass": int(rpo_pass),
        "checksum_match": int(checksum_match),
        "checksum_result": "PASS" if checksum_match else "FAIL",
        "state_match": int(state_match),
        "state_validation_result": "PASS" if state_match else "FAIL",
        "state_integrity_result": "PASS" if state_match else "FAIL",
        "overall_result": "PASS" if overall_pass else "FAIL",
        "error_reason": error_reason,
        "error_message": error_reason,
        "recommendation": recommendation
    }

