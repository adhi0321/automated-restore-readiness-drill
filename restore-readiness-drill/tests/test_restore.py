import unittest
from backend.backup_service import SessionSimulator, create_backup
from backend.restore_service import perform_restore

class TestRestore(unittest.TestCase):
    def test_successful_restore(self):
        sim = SessionSimulator("test2")
        events = sim.generate_events(5)
        backup = create_backup("test2", events)
        
        result = perform_restore(backup)
        self.assertEqual(result.status, "SUCCESS")
        self.assertIsNotNone(result.restored_state)
        self.assertEqual(result.restored_state.version, 5)
        self.assertGreater(result.recovery_time_seconds, 0)

if __name__ == "__main__":
    unittest.main()

