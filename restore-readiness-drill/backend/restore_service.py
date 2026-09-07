import time
import uuid
from .models import BackupData, SessionState, RestoreAttemptResult

def rebuild_state(backup: BackupData) -> SessionState:
    """
    Rebuilds the session state by replaying events safely.
    Handles duplicate prevention and ordering.
    """
    seen_ids = set()
    
    # Critical: Sort by version to handle out-of-order events
    sorted_events = sorted(backup.events, key=lambda e: e.version)
    
    current_state = {}
    current_version = 0
    
    for event in sorted_events:
        if event.event_id in seen_ids:
            continue # Skip duplicates
        seen_ids.add(event.event_id)
        
        current_state.update(event.payload)
        if event.version > current_version:
            current_version = event.version
            
    return SessionState(
        session_id="reconstructed_session",
        player_count=current_state.get("player_count", 0),
        version=current_version,
        state=current_state,
        updated_at=time.time()
    )

def perform_restore(backup: BackupData) -> RestoreAttemptResult:
    start_time = time.time()
    attempt_id = str(uuid.uuid4())
    
    try:
        # Provide realistic (simulated) delay
        time.sleep(0.1) 
        restored_state = rebuild_state(backup)
        
        end_time = time.time()
        return RestoreAttemptResult(
            attempt_id=attempt_id,
            backup_id=backup.backup_id,
            started_at=start_time,
            completed_at=end_time,
            recovery_time_seconds=end_time - start_time,
            status="SUCCESS",
            restored_state=restored_state
        )
    except Exception as e:
        end_time = time.time()
        return RestoreAttemptResult(
            attempt_id=attempt_id,
            backup_id=backup.backup_id,
            started_at=start_time,
            completed_at=end_time,
            recovery_time_seconds=end_time - start_time,
            status="ERROR",
            error_message=str(e)
        )
