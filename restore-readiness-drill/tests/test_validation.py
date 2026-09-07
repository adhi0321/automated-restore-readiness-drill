import pytest
import time
from backend.backup_service import SessionSimulator, create_backup
from backend.validation_service import run_drill
from backend.restore_service import rebuild_state
from backend.config import Config

def test_rto_rpo_validation():
    sim = SessionSimulator("rto_test")
    events = sim.generate_events(5)
    backup = create_backup("rto_test", events)
    expected_state = rebuild_state(backup)
    
    # 1. Test Passing RTO/RPO
    # We pass time.time() as failure time. RPO should be very small since events were just made.
    result_pass = run_drill(backup, expected_state, time.time())
    assert result_pass["rto_pass"] == 1
    assert result_pass["rpo_pass"] == 1
    
    # 2. Test Failing RPO
    # If the crash happened 1000 seconds in the future, the backup is too old.
    future_time = time.time() + Config.RPO_TARGET_SECONDS + 100
    result_fail_rpo = run_drill(backup, expected_state, future_time)
    assert result_fail_rpo["rpo_pass"] == 0
    assert result_fail_rpo["overall_result"] == "FAIL"
