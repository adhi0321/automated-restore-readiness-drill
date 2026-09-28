import unittest
import time
from backend.database import init_db, save_drill_result, get_all_drill_results
from backend.metrics import calculate_metrics
from backend.backup_service import SessionSimulator, create_backup
from backend.validation_service import run_drill
from backend.restore_service import rebuild_state

class TestDatabaseAndMetrics(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_save_and_retrieve_drill(self):
        sim = SessionSimulator("api_test_session")
        events = sim.generate_events(10)
        backup = create_backup("api_test_session", events)
        expected_state = rebuild_state(backup)
        drill_record = run_drill(backup, expected_state, time.time())
        
        save_drill_result(drill_record)
        all_results = get_all_drill_results()
        self.assertGreater(len(all_results), 0)
        
        # Verify saved record attributes
        found = any(r['drill_id'] == drill_record['drill_id'] for r in all_results)
        self.assertTrue(found)

    def test_metrics_calculation(self):
        mock_results = [
            {"overall_result": "PASS", "recovery_time_seconds": 0.12},
            {"overall_result": "PASS", "recovery_time_seconds": 0.18},
            {"overall_result": "FAIL", "recovery_time_seconds": 0.15},
        ]
        metrics = calculate_metrics(mock_results)
        self.assertEqual(metrics["total_drills"], 3)
        self.assertEqual(metrics["successful_drills"], 2)
        self.assertEqual(metrics["failed_drills"], 1)
        self.assertAlmostEqual(metrics["recovery_success_rate"], 66.67, places=1)
        self.assertAlmostEqual(metrics["average_recovery_time"], 0.15, places=2)

if __name__ == "__main__":
    unittest.main()
