from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SessionEvent(BaseModel):
    event_id: str
    timestamp: float
    version: int
    event_type: str
    payload: Dict[str, Any]

class SessionState(BaseModel):
    session_id: str
    player_count: int
    version: int
    state: Dict[str, Any]
    updated_at: float

class BackupData(BaseModel):
    backup_id: str
    created_at: float
    source_session_version: int
    events: List[SessionEvent]
    checksum: str = ""

class RestoreAttemptResult(BaseModel):
    attempt_id: str
    backup_id: str
    started_at: float
    completed_at: float
    recovery_time_seconds: float
    status: str
    error_message: Optional[str] = None
    restored_state: Optional[SessionState] = None

class ValidationResult(BaseModel):
    validation_id: str
    attempt_id: str
    checksum_match: bool
    record_count_match: bool
    state_match: bool
    corrupted_records: int
    validation_status: str

class DrillResult(BaseModel):
    drill_id: str
    attempt_id: str
    rto_target: float
    rpo_target: float
    actual_rto: float
    actual_rpo: float
    rto_pass: bool
    rpo_pass: bool
    overall_result: str
    recommendation: str
