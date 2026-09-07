import pytest
from backend.backup_service import SessionSimulator, create_backup
from backend.restore_service import perform_restore

def test_successful_restore():
    sim = SessionSimulator("test2")
    events = sim.generate_events(5)
    backup = create_backup("test2", events)
    
    result = perform_restore(backup)
    assert result.status == "SUCCESS"
    assert result.restored_state is not None
    assert result.restored_state.version == 5
    assert result.recovery_time_seconds > 0
