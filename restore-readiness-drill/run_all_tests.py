#!/usr/bin/env python3
"""
Automated Test Suite Runner for Restore-Readiness Drill
Runs all unit and integration tests across backup, restore, validation,
failure injection (all 9 scenarios), metrics, and REST API endpoints.
Outputs exact numbers for Total, Passed, Failed, and Skipped tests.
"""

import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

TESTS_DIR = os.path.join(CURRENT_DIR, "tests")

def run_tests():
    print("=" * 70)
    print("AUTOMATED RESTORE-READINESS DRILL: COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"Test Directory: {TESTS_DIR}\n")
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    total = result.testsRun
    failed = len(result.failures) + len(result.errors)
    skipped = len(result.skipped)
    passed = total - failed - skipped
    
    print("\n" + "=" * 70)
    print("TEST EXECUTION RESULTS")
    print("=" * 70)
    print(f"Total Tests:   {total}")
    print(f"Passed:        {passed}")
    print(f"Failed:        {failed}")
    print(f"Skipped:       {skipped}")
    print("=" * 70)
    
    if failed == 0:
        print("ALL TESTS PASSED SUCCESSFULLY! (100% PASS RATE)")
        return 0
    else:
        print(f"FAILURE: {failed} test(s) failed.")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
