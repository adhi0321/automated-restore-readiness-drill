import unittest
from backend.backup_service import SessionSimulator, create_backup
from backend.restore_service import rebuild_state

class TestBackup(unittest.TestCase):
    def test_backup_generation(self):
        sim = SessionSimulator("test1")
        events = sim.generate_events(10)
        
        backup = create_backup("test1", events)
        self.assertEqual(backup.source_session_version, 10)
        self.assertEqual(len(backup.events), 10)
        self.assertTrue(backup.checksum != "")

if __name__ == "__main__":
    unittest.main()

