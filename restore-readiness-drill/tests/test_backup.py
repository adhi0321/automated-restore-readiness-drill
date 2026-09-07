import pytest
from backend.backup_service import SessionSimulator, create_backup
from backend.restore_service import rebuild_state

def test_backup_generation():
    sim = SessionSimulator("test1")
    events = sim.generate_events(10)
    
    backup = create_backup("test1", events)
    assert backup.source_session_version == 10
    assert len(backup.events) == 10
    assert backup.checksum != ""
