import time
import os
import json
from backend.database import init_db, save_drill_result
from backend.backup_service import SessionSimulator, create_backup
from backend.validation_service import run_drill
from backend.failure_injection import (
    inject_corrupted_backup, 
    inject_duplicate_event, 
    inject_out_of_order_events, 
    inject_delayed_event
)

def run_demo():
    print("Initializing Database...")
    init_db()
    
    print("Generating simulated multiplayer session state...")
    sim = SessionSimulator(session_id="demo_session_1")
    sim.generate_events(100) # 100 state changes
    
    # Store original complete state to compare against
    from backend.restore_service import rebuild_state
    
    # We construct a mock backup just to reconstruct the original state baseline easily
    temp_backup = create_backup(sim.session_id, sim.events)
    original_state = rebuild_state(temp_backup)
    
    print("Running 10 Drills (6 Normal, 4 Failure Injected)...")
    
    drills = []
    
    # 6 Normal Drills
    for i in range(6):
        backup = create_backup(sim.session_id, sim.events)
        failure_time = time.time()
        result = run_drill(backup, original_state, failure_time)
        drills.append(result)

    # 1 Corrupted Drill
    corrupt_backup = inject_corrupted_backup(create_backup(sim.session_id, sim.events))
    drills.append(run_drill(corrupt_backup, original_state, time.time()))

    # 1 Duplicate Event Drill
    dupe_backup = inject_duplicate_event(create_backup(sim.session_id, sim.events))
    drills.append(run_drill(dupe_backup, original_state, time.time()))

    # 1 Out-of-Order Drill
    ooo_backup = inject_out_of_order_events(create_backup(sim.session_id, sim.events))
    drills.append(run_drill(ooo_backup, original_state, time.time()))
    
    # 1 Delayed Event Drill
    delayed_backup = inject_delayed_event(create_backup(sim.session_id, sim.events))
    drills.append(run_drill(delayed_backup, original_state, time.time()))

    print(f"\nCompleted {len(drills)} drills. Saving to Database...")
    for d in drills:
        save_drill_result(d)
        print(f"Drill {d['drill_id'][:8]} - Result: {d['overall_result']}")

    # Save samples to data dir for reference
    os.makedirs("data", exist_ok=True)
    with open("data/sample_backup.json", "w") as f:
        f.write(temp_backup.model_dump_json(indent=2))

    print("\nExperiment Complete. Run `uvicorn backend.main:app --reload` to view the dashboard.")

if __name__ == "__main__":
    run_demo()
