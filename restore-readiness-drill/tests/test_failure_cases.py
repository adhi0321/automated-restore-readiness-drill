import unittest
import time
from backend.backup_service import SessionSimulator, create_backup
from backend.validation_service import run_drill
from backend.restore_service import rebuild_state
from backend.failure_injection import (
    inject_corrupted_backup, 
    inject_duplicate_event, 
    inject_out_of_order_events,
    inject_delayed_event,
    inject_truncated_wal,
    inject_concurrent_conflict
)

class TestFailureCases(unittest.TestCase):
    def setUp(self):
        self.sim = SessionSimulator("test3")
        self.events = self.sim.generate_events(15)
        self.backup = create_backup("test3", self.events)
        self.expected = rebuild_state(self.backup)

    def test_corrupted_backup(self):
        corrupt = inject_corrupted_backup(self.backup)
        result = run_drill(corrupt, self.expected, time.time())
        self.assertEqual(result["checksum_match"], 0)
        self.assertEqual(result["overall_result"], "FAIL")

    def test_duplicate_events(self):
        dupe = inject_duplicate_event(self.backup)
        result = run_drill(dupe, self.expected, time.time())
        # State should still match because engine deduplicates!
        self.assertEqual(result["state_match"], 1)
        self.assertEqual(result["checksum_match"], 1)
        self.assertEqual(result["overall_result"], "PASS")

    def test_out_of_order_events(self):
        ooo = inject_out_of_order_events(self.backup)
        result = run_drill(ooo, self.expected, time.time())
        # State should still match because engine sorts by version
        self.assertEqual(result["state_match"], 1)
        self.assertEqual(result["overall_result"], "PASS")

    def test_delayed_events(self):
        delayed = inject_delayed_event(self.backup)
        result = run_drill(delayed, self.expected, time.time())
        # State should remain consistent without corruption
        self.assertEqual(result["checksum_match"], 1)
        self.assertEqual(result["overall_result"], "PASS")

    def test_truncated_wal(self):
        truncated = inject_truncated_wal(self.backup)
        result = run_drill(truncated, self.expected, time.time())
        # Partial WAL should execute safely and report status
        self.assertIn(result["overall_result"], ["PASS", "FAIL"])

    def test_concurrent_conflict(self):
        conflict = inject_concurrent_conflict(self.backup)
        result = run_drill(conflict, self.expected, time.time())
        self.assertIn(result["overall_result"], ["PASS", "FAIL"])

if __name__ == "__main__":
    unittest.main()


