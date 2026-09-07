import json
import hashlib
import time
import uuid
from typing import List, Dict
from .models import SessionEvent, BackupData

class SessionSimulator:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.events: List[SessionEvent] = []
        self.version = 0

    def generate_events(self, count: int):
        for i in range(count):
            self.version += 1
            event = SessionEvent(
                event_id=str(uuid.uuid4()),
                timestamp=time.time() - (count - i) * 2.0, # Past timestamps
                version=self.version,
                event_type="update",
                payload={"player_count": 10 + (i % 5), "score": i * 100}
            )
            self.events.append(event)
        return self.events

def generate_checksum(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def create_backup(session_id: str, events: List[SessionEvent]) -> BackupData:
    backup_id = str(uuid.uuid4())
    # Sort just to be clean initially
    sorted_events = sorted(events, key=lambda x: x.version)
    latest_version = sorted_events[-1].version if sorted_events else 0
    
    backup = BackupData(
        backup_id=backup_id,
        created_at=time.time(),
        source_session_version=latest_version,
        events=sorted_events
    )
    
    # Calculate checksum excluding the checksum field itself
    backup_json = backup.model_dump_json(exclude={"checksum"})
    backup.checksum = generate_checksum(backup_json)
    
    return backup
