from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass, field, asdict

try:
    from pydantic import BaseModel as _PydanticBaseModel
    class BaseModel(_PydanticBaseModel):
        pass
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        
        def model_dump(self, exclude: Optional[set] = None) -> Dict[str, Any]:
            def _serialize(val):
                if hasattr(val, "model_dump"):
                    return val.model_dump()
                elif isinstance(val, list):
                    return [_serialize(x) for x in val]
                elif isinstance(val, dict):
                    return {k: _serialize(v) for k, v in val.items()}
                return val
            
            res = {}
            for k, v in self.__dict__.items():
                if exclude and k in exclude:
                    continue
                res[k] = _serialize(v)
            return res

        def model_dump_json(self, exclude: Optional[set] = None, indent: Optional[int] = None) -> str:
            d = self.model_dump(exclude=exclude)
            return json.dumps(d, indent=indent, sort_keys=True)

class SessionEvent(BaseModel):
    event_id: str
    timestamp: float
    version: int
    event_type: str
    payload: Dict[str, Any]

    def __init__(self, event_id: str = "", timestamp: float = 0.0, version: int = 0, event_type: str = "", payload: Optional[Dict[str, Any]] = None, **kwargs):
        self.event_id = event_id or kwargs.get("event_id", "")
        self.timestamp = timestamp or kwargs.get("timestamp", 0.0)
        self.version = version or kwargs.get("version", 0)
        self.event_type = event_type or kwargs.get("event_type", "")
        self.payload = payload if payload is not None else kwargs.get("payload", {})

class SessionState(BaseModel):
    session_id: str
    player_count: int
    version: int
    state: Dict[str, Any]
    updated_at: float

    def __init__(self, session_id: str = "", player_count: int = 0, version: int = 0, state: Optional[Dict[str, Any]] = None, updated_at: float = 0.0, **kwargs):
        self.session_id = session_id or kwargs.get("session_id", "")
        self.player_count = player_count or kwargs.get("player_count", 0)
        self.version = version or kwargs.get("version", 0)
        self.state = state if state is not None else kwargs.get("state", {})
        self.updated_at = updated_at or kwargs.get("updated_at", 0.0)

class BackupData(BaseModel):
    backup_id: str
    created_at: float
    source_session_version: int
    events: List[SessionEvent]
    checksum: str = ""

    def __init__(self, backup_id: str = "", created_at: float = 0.0, source_session_version: int = 0, events: Optional[List[SessionEvent]] = None, checksum: str = "", **kwargs):
        self.backup_id = backup_id or kwargs.get("backup_id", "")
        self.created_at = created_at or kwargs.get("created_at", 0.0)
        self.source_session_version = source_session_version or kwargs.get("source_session_version", 0)
        self.events = events if events is not None else kwargs.get("events", [])
        self.checksum = checksum or kwargs.get("checksum", "")

class RestoreAttemptResult(BaseModel):
    attempt_id: str
    backup_id: str
    started_at: float
    completed_at: float
    recovery_time_seconds: float
    status: str
    error_message: Optional[str] = None
    restored_state: Optional[SessionState] = None

    def __init__(self, attempt_id: str = "", backup_id: str = "", started_at: float = 0.0, completed_at: float = 0.0, recovery_time_seconds: float = 0.0, status: str = "", error_message: Optional[str] = None, restored_state: Optional[SessionState] = None, **kwargs):
        self.attempt_id = attempt_id or kwargs.get("attempt_id", "")
        self.backup_id = backup_id or kwargs.get("backup_id", "")
        self.started_at = started_at or kwargs.get("started_at", 0.0)
        self.completed_at = completed_at or kwargs.get("completed_at", 0.0)
        self.recovery_time_seconds = recovery_time_seconds or kwargs.get("recovery_time_seconds", 0.0)
        self.status = status or kwargs.get("status", "")
        self.error_message = error_message if error_message is not None else kwargs.get("error_message")
        self.restored_state = restored_state if restored_state is not None else kwargs.get("restored_state")

class ValidationResult(BaseModel):
    validation_id: str
    attempt_id: str
    checksum_match: bool
    record_count_match: bool
    state_match: bool
    corrupted_records: int
    validation_status: str

    def __init__(self, validation_id: str = "", attempt_id: str = "", checksum_match: bool = False, record_count_match: bool = False, state_match: bool = False, corrupted_records: int = 0, validation_status: str = "", **kwargs):
        self.validation_id = validation_id or kwargs.get("validation_id", "")
        self.attempt_id = attempt_id or kwargs.get("attempt_id", "")
        self.checksum_match = checksum_match if checksum_match is not None else kwargs.get("checksum_match", False)
        self.record_count_match = record_count_match if record_count_match is not None else kwargs.get("record_count_match", False)
        self.state_match = state_match if state_match is not None else kwargs.get("state_match", False)
        self.corrupted_records = corrupted_records or kwargs.get("corrupted_records", 0)
        self.validation_status = validation_status or kwargs.get("validation_status", "")

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

    def __init__(self, drill_id: str = "", attempt_id: str = "", rto_target: float = 0.0, rpo_target: float = 0.0, actual_rto: float = 0.0, actual_rpo: float = 0.0, rto_pass: bool = False, rpo_pass: bool = False, overall_result: str = "", recommendation: str = "", **kwargs):
        self.drill_id = drill_id or kwargs.get("drill_id", "")
        self.attempt_id = attempt_id or kwargs.get("attempt_id", "")
        self.rto_target = rto_target or kwargs.get("rto_target", 0.0)
        self.rpo_target = rpo_target or kwargs.get("rpo_target", 0.0)
        self.actual_rto = actual_rto or kwargs.get("actual_rto", 0.0)
        self.actual_rpo = actual_rpo or kwargs.get("actual_rpo", 0.0)
        self.rto_pass = rto_pass if rto_pass is not None else kwargs.get("rto_pass", False)
        self.rpo_pass = rpo_pass if rpo_pass is not None else kwargs.get("rpo_pass", False)
        self.overall_result = overall_result or kwargs.get("overall_result", "")
        self.recommendation = recommendation or kwargs.get("recommendation", "")

