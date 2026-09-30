# 10-STEP PROJECT DEMONSTRATION SCRIPT

This step-by-step demonstration walkthrough is designed for project presentations, academic defense sessions, and stakeholder reviews. It allows an evaluator to test all core capabilities of the Restore-Readiness Drill platform in under 5 minutes.

---

## Demonstration Workflow

### Step 1: Open the Interactive Dashboard
- **Action:** Open the web browser to `http://localhost:3000/` (or the Google AI Studio Preview root URL).
- **Talking Point:** *"Notice the High-Density dark engineering layout. At the top, we see our executive SLA targets: RTO Target of 60 seconds and RPO Target of 30 seconds, alongside our real-time recovery metrics."*

---

### Step 2: Run a Normal Baseline Drill
- **Action:** Click the **"Normal Restore"** button (or **"Run Restore Drill"**).
- **Observed Result:**
  - A green badge flashes: **PASS**.
  - RTO is computed in milliseconds (~0.01s).
  - SHA-256 Checksum Match: **PASS**.
  - State Fidelity: **PASS**.
- **Talking Point:** *"Under healthy operating conditions, the drill packages a live session, calculates the SHA-256 fingerprint, restores into a sandbox, and verifies that the reconstructed player state matches truth field-for-field."*

---

### Step 3: Trigger Corrupted Backup Scenario (Bit-Rot)
- **Action:** Click the **"Corrupted Backup"** chaos button.
- **Observed Result:**
  - An immediate red banner: **FAIL**.
  - Checksum Status: **MISMATCH (BIT-ROT DETECTED)**.
  - State Commit: **ABORTED**.
- **Talking Point:** *"In a traditional system, this backup would look fine because the file exists. But our SHA-256 gate immediately catches the corrupted payload, preventing broken data from ever polluting production servers."*

---

### Step 4: Inject Duplicate Event Flooding (Network Retries)
- **Action:** Click the **"Duplicate Event"** chaos button.
- **Observed Result:**
  - Drill Result: **PASS**.
  - Duplicate events are flagged and dropped by the idempotency cache.
  - Player inventory and scores are not duplicated.
- **Talking Point:** *"Notice that despite duplicate packets being injected, the drill passes. Our restore engine uses an idempotent event cache that discards repeated packets so player currency and items aren't double-credited."*

---

### Step 5: Inject Out-of-Order Packets (Network Jitter)
- **Action:** Click the **"Out-of-Order Event"** chaos button.
- **Observed Result:**
  - Drill Result: **PASS**.
  - Packets arriving shuffled are sorted into correct monotonic version sequence.
- **Talking Point:** *"Network jitter often causes later packets to arrive before earlier ones. The engine sorts events by sequence version prior to applying state mutations, ensuring players don't teleport back in time."*

---

### Step 6: Inject Delayed Straggler Events
- **Action:** Click the **"Delayed Event"** chaos button.
- **Observed Result:**
  - Drill Result: **PASS**.
  - Stale events older than the current version are safely handled without overwriting newer state.
- **Talking Point:** *"If an old packet arrives late after a disconnect, the Lamport version gate prevents it from overwriting newer match events."*

---

### Step 7: Run the Full Controlled Experiment (30 Drills)
- **Action:** From the terminal, run:
  ```bash
  python3 run_final_experiment.py
  ```
  *(Or click "Run 30-Drill Experiment Batch" in the UI).*
- **Observed Result:**
  - The script executes 30 drills with fixed seed 42 across all 9 failure categories in under 2 seconds.
- **Talking Point:** *"We now execute our 30-drill controlled experiment with a fixed random seed. It runs 10 normal backups and 20 chaos injections, updating our SQLite database and generating all audit evidence files."*

---

### Step 8: View Measured Metrics and Recovery Rate
- **Action:** Inspect the **Final Experiment Results** section on the dashboard.
- **Observed Result:**
  - Total Drills: **30**
  - Successful Drills: **19**
  - Failed Drills (Detected): **11**
  - Measured Recovery Rate: **63.33%**
  - Average Recovery Duration: **5.00 seconds**
- **Talking Point:** *"Here is the critical distinction: our prototype does not claim 100% readiness. It accurately shows that 63.33% of backups are safe for immediate disaster recovery within RTO and RPO, and safely flags the remaining 36.67%."*

---

### Step 9: Review the Baseline vs Prototype Matrix
- **Action:** Scroll to the **Baseline vs Prototype Comparison** card.
- **Observed Result:**
  - Shows that the traditional baseline had **20 undetected failures**, while the prototype had **0 undetected failures**.
- **Talking Point:** *"This side-by-side comparison demonstrates the core academic contribution: eliminating false confidence. While the baseline would have caused an outage on 20 out of 30 backups, our system caught every single failure before disaster."*

---

### Step 10: Download the SOC 2 / DR Audit Report
- **Action:** Click **"Export Audit Report (JSON / Markdown)"** or view the printable **Compliance Certificate**.
- **Observed Result:**
  - A comprehensive technical audit report with timestamped cryptographic hashes and step durations is generated.
- **Talking Point:** *"With one click, compliance officers and executive stakeholders can export a complete, verifiable audit trail ready for SOC 2 or ISO 27001 disaster recovery audits."*
