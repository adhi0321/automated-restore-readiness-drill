from fastapi import FastAPI, Query, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from .database import init_db, get_all_drill_results, save_drill_result
from .metrics import calculate_metrics
from .backup_service import SessionSimulator, create_backup
from .restore_service import rebuild_state
from .validation_service import run_drill
from .failure_injection import (
    inject_corrupted_backup,
    inject_duplicate_event,
    inject_out_of_order_events,
    inject_delayed_event,
    inject_truncated_wal,
    inject_concurrent_conflict,
    inject_rto_breach,
    inject_rpo_breach,
)

import os
import time

app = FastAPI(
    title="Automated Restore-Readiness Drill",
    description="Backend API for multiplayer session state restore verification, chaos failure injection, and SLA compliance",
    version="0.7.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/results")
def get_results():
    results = get_all_drill_results()
    metrics = calculate_metrics(results)
    return {
        "metrics": metrics,
        "results": results
    }

@app.get("/api/metrics")
def get_detailed_metrics():
    results = get_all_drill_results()
    metrics = calculate_metrics(results)
    
    total = len(results)
    rto_passed = sum(1 for r in results if r.get('rto_pass') == 1)
    rpo_passed = sum(1 for r in results if r.get('rpo_pass') == 1)
    checksum_passed = sum(1 for r in results if r.get('checksum_match') == 1)
    state_passed = sum(1 for r in results if r.get('state_match') == 1)
    
    failure_causes = {}
    for r in results:
        if r.get('overall_result') != 'PASS':
            reason = "Checksum Mismatch" if not r.get('checksum_match') else \
                     "State Mismatch" if not r.get('state_match') else \
                     "RTO Breach" if not r.get('rto_pass') else \
                     "RPO Breach" if not r.get('rpo_pass') else "Execution Error"
            failure_causes[reason] = failure_causes.get(reason, 0) + 1

    return {
        "summary": metrics,
        "compliance": {
            "rto_compliance_rate": round((rto_passed / total * 100), 2) if total > 0 else 0,
            "rpo_compliance_rate": round((rpo_passed / total * 100), 2) if total > 0 else 0,
            "checksum_integrity_rate": round((checksum_passed / total * 100), 2) if total > 0 else 0,
            "state_fidelity_rate": round((state_passed / total * 100), 2) if total > 0 else 0,
        },
        "failure_breakdown": failure_causes
    }

@app.post("/api/drills/run")
def execute_drill(scenario: str = Query("NORMAL", description="Failure scenario to inject")):
    scenario = scenario.upper()
    sim = SessionSimulator(session_id="session_" + str(int(time.time())))
    sim.generate_events(25)
    
    base_backup = create_backup(sim.session_id, sim.events)
    expected_state = rebuild_state(base_backup)
    failure_time = time.time()
    
    if scenario in ("CORRUPTED", "CORRUPT_CHECKSUM"):
        test_backup = inject_corrupted_backup(base_backup)
    elif scenario in ("DUPLICATE", "DUPLICATE_EVENT"):
        test_backup = inject_duplicate_event(base_backup)
    elif scenario in ("OUT_OF_ORDER", "OUT_OF_ORDER_EVENT"):
        test_backup = inject_out_of_order_events(base_backup)
    elif scenario in ("DELAYED", "DELAYED_STRAGGLER", "DELAYED_EVENT"):
        test_backup = inject_delayed_event(base_backup)
    elif scenario == "TRUNCATED_WAL":
        test_backup = inject_truncated_wal(base_backup)
    elif scenario == "CONCURRENT_CONFLICT":
        test_backup = inject_concurrent_conflict(base_backup)
    elif scenario == "RTO_BREACH":
        test_backup = inject_rto_breach(base_backup)
    elif scenario == "RPO_BREACH":
        test_backup = inject_rpo_breach(base_backup, failure_time)
    else:
        test_backup = base_backup
        
    result = run_drill(test_backup, expected_state, failure_time, scenario=scenario, session_id=sim.session_id)
    save_drill_result(result)
    return result


@app.post("/api/experiments/batch")
def run_batch_experiment(count: int = Query(10, ge=1, le=50)):
    scenarios = ["NORMAL", "NORMAL", "CORRUPTED", "DUPLICATE", "OUT_OF_ORDER", "DELAYED", "TRUNCATED_WAL"]
    batch_results = []
    
    for i in range(count):
        scenario = scenarios[i % len(scenarios)]
        res = execute_drill(scenario)
        batch_results.append(res)
        
    all_results = get_all_drill_results()
    metrics = calculate_metrics(all_results)
    return {
        "status": "COMPLETED",
        "batch_count": count,
        "batch_drills": batch_results,
        "overall_metrics": metrics
    }

@app.get("/api/risk-register")
def get_risk_register():
    return {
        "risks": [
            {
                "id": "RSK-001",
                "category": "Storage Corruption",
                "description": "Silent bit rot in backup snapshot archive leaves backup unreadable during catastrophic crash.",
                "likelihood": "LOW",
                "impact": "CRITICAL",
                "mitigation": "Automated SHA-256 pre-restore verification and multi-zone replica checksum cross-referencing.",
                "verification_drill": "CORRUPT_CHECKSUM drill"
            },
            {
                "id": "RSK-002",
                "category": "Concurrency & Idempotency",
                "description": "Reconnection retry storms generate duplicate mutation events, double-charging currency or duplicating inventory.",
                "likelihood": "HIGH",
                "impact": "HIGH",
                "mitigation": "Idempotent event ingestion with deduplication bloom filter and version tracking in restore engine.",
                "verification_drill": "DUPLICATE_EVENT drill"
            },
            {
                "id": "RSK-003",
                "category": "Network & Asynchrony",
                "description": "UDP jitter and retransmissions cause out-of-order state mutations, unwinding game world sequence.",
                "likelihood": "HIGH",
                "impact": "MEDIUM",
                "mitigation": "Strict monotonic sequence sort and Lamport timestamp replay validation prior to state materialization.",
                "verification_drill": "OUT_OF_ORDER drill"
            },
            {
                "id": "RSK-004",
                "category": "SLA & Performance",
                "description": "Restore reconstruction exceeds 60s RTO target due to unbounded WAL replay volume.",
                "likelihood": "MEDIUM",
                "impact": "HIGH",
                "mitigation": "Periodic snapshot compaction every 30s and parallel replay sandboxing.",
                "verification_drill": "RTO_BREACH drill"
            },
            {
                "id": "RSK-005",
                "category": "Partial Logging",
                "description": "Abrupt host crash terminates WAL flush halfway through buffer write, truncating tail records.",
                "likelihood": "MEDIUM",
                "impact": "HIGH",
                "mitigation": "Atomic commit framing with CRC32 block headers and automatic fallback to previous valid checkpoint.",
                "verification_drill": "TRUNCATED_WAL drill"
            }
        ]
    }

@app.get("/api/baseline-comparison")
def get_baseline_comparison():
    return {
        "baseline": {
            "name": "Traditional Backup Status Verification",
            "restore_frequency": "Annually or never",
            "integrity_check": "Exit code 0 of snapshot creation tool",
            "rto_verified": False,
            "rpo_verified": False,
            "session_state_safe": False,
            "detection_time": "During real disaster (hours or days)",
            "average_downtime": "4.5 hours",
            "data_loss_risk": "High (untested delta drift)"
        },
        "automated_drill_prototype": {
            "name": "Continuous Automated Restore-Readiness Drill",
            "restore_frequency": "Continuous / automated on every checkpoint",
            "integrity_check": "End-to-end sandbox restore with SHA-256 cryptographic state audit",
            "rto_verified": True,
            "rpo_verified": True,
            "session_state_safe": True,
            "detection_time": "Instantaneous (<120ms)",
            "average_downtime": "< 60 seconds (target SLA)",
            "data_loss_risk": "Minimal (< 30 seconds RPO guarantee)"
        }
    }

@app.get("/api/report/export")
def export_report():
    results = get_all_drill_results()
    metrics = calculate_metrics(results)
    
    markdown_lines = [
        "# Automated Restore-Readiness Drill - Technical Audit Report",
        f"**Generated At:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}",
        f"**System Scope:** Multiplayer Session-State Disaster Recovery",
        "",
        "## Executive Summary",
        f"- **Total Drills Conducted:** {metrics.get('total_drills', 0)}",
        f"- **Successful Restores:** {metrics.get('successful_drills', 0)}",
        f"- **Failed Restores:** {metrics.get('failed_drills', 0)}",
        f"- **Recovery Success Rate:** {metrics.get('recovery_success_rate', 0)}%",
        f"- **Average Recovery Time:** {metrics.get('average_recovery_time', 0)}s (Target: <= 60.0s)",
        "",
        "## Recent Drill Audit Trail",
        "| Drill ID | Backup ID | Result | Checksum Match | State Match | RTO (s) | RPO (s) |",
        "|---|---|---|---|---|---|---|"
    ]
    for r in results[:15]:
        markdown_lines.append(
            f"| `{r['drill_id'][:8]}` | `{r['backup_id'][:8]}` | **{r['overall_result']}** | {'YES' if r['checksum_match'] else 'NO'} | {'YES' if r['state_match'] else 'NO'} | {r['recovery_time_seconds']:.3f} | {r['actual_rpo']:.1f} |"
        )
    
    return {
        "metrics": metrics,
        "sample_size": len(results),
        "markdown_report": "\n".join(markdown_lines)
    }

# Serve frontend statically
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"status": "Restore-Readiness Drill API Active", "version": "0.7.0"})

