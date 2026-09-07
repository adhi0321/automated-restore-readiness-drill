import pytest
import time
from backend.backup_service import SessionSimulator, create_backup
from backend.validation_service import run_drill
from backend.restore_service import rebuild_state
from backend.failure_injection import (
    inject_corrupted_backup, 
    inject_duplicate_event, 
    inject_out_of_order_events
)

@pytest.fixture
def base_data():
    sim = SessionSimulator("test3")
    events = sim.generate_events(15)
    backup = create_backup("test3", events)
    expected_state = rebuild_state(backup)
    return backup, expected_state

def test_corrupted_backup(base_data):
    backup, expected = base_data
    corrupt = inject_corrupted_backup(backup)
    result = run_drill(corrupt, expected, time.time())
    
    assert result["checksum_match"] == 0
    assert result["overall_result"] == "FAIL"

def test_duplicate_events(base_data):
    backup, expected = base_data
    dupe = inject_duplicate_event(backup)
    result = run_drill(dupe, expected, time.time())
    
    # State should still match because engine deduplicates!
    assert result["state_match"] == 1
    assert result["checksum_match"] == 1
    assert result["overall_result"] == "PASS"

def test_out_of_order_events(base_data):
    backup, expected = base_data
    ooo = inject_out_of_order_events(backup)
    result = run_drill(ooo, expected, time.time())
    
    # State should still match because engine sorts by version
    assert result["state_match"] == 1
    assert result["overall_result"] == "PASS"
