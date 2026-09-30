#!/usr/bin/env python3
"""
Root runner for the Final Reproducible Experiment.
Dispatches to restore-readiness-drill/run_final_experiment.py.
"""
import os
import sys
import importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_SCRIPT = os.path.join(SCRIPT_DIR, "restore-readiness-drill", "run_final_experiment.py")

if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("final_experiment_module", TARGET_SCRIPT)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.run_experiment()
    else:
        print(f"Error loading {TARGET_SCRIPT}")
        sys.exit(1)

