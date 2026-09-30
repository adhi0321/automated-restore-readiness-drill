#!/usr/bin/env python3
"""Root test runner dispatcher for restore-readiness-drill/run_all_tests.py"""
import os
import sys
import runpy

root_dir = os.path.dirname(os.path.abspath(__file__))
sub_dir = os.path.join(root_dir, "restore-readiness-drill")
if sub_dir not in sys.path:
    sys.path.insert(0, sub_dir)

target_script = os.path.join(sub_dir, "run_all_tests.py")

if __name__ == "__main__":
    runpy.run_path(target_script, run_name="__main__")
