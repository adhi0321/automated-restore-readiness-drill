# SYSTEM BOUNDARIES AND PROTOTYPE LIMITATIONS

## 1. Academic Scope and Prototype Boundaries
This project is an academic proof-of-concept and engineering prototype designed to demonstrate the principles of automated restore-readiness verification. While the architecture, algorithmic deduplication, cryptographic hashing, and SLA measurement logic are production-grade concepts, the execution environment contains deliberate boundaries.

We document these limitations candidly below.

---

## 2. Technical Limitations

### A. Simulated Multiplayer Workload vs. Live Production
- **Prototype Scale:** The session simulator models 4 game lobbies with 20 to 40 events per session (representing a few minutes of gameplay for testing).
- **Production Reality:** A commercial multiplayer title (e.g., an MMO or Battle Royale) handles tens of thousands of concurrent players generating 30–60 tick mutations per second across distributed geographic regions.
- **Impact:** System behavior under multi-gigabyte state payloads or severe network thrashing has not been measured.

### B. Local SQLite Persistence vs. Distributed Data Stores
- **Prototype Environment:** State telemetry and drill results are stored in a local SQLite file (`drill_results.db`) using single-node file locking.
- **Production Reality:** Modern game studios utilize distributed databases (e.g., PostgreSQL with Citus, CockroachDB, Amazon DynamoDB, or Redis Enterprise Clusters) with complex distributed consensus and multi-region replication.
- **Impact:** Lock contention, disk write stalls, and replication lag between distributed nodes are not modeled by SQLite.

### C. Synthetic Failure Injection vs. Physical Hardware Faults
- **Prototype Mechanism:** Failures (checksum corruption, packet reordering, delays) are injected programmatically in Python memory.
- **Production Reality:** Real outages arise from physical switch failures, undersea cable cuts, cloud availability zone brownouts, kernel panics, or ungraceful Docker container OOM kills.
- **Impact:** The prototype validates the *logical handling* of anomalies, but cannot simulate OS-level I/O hung tasks or kernel crash dumps.

### D. Simulated Backup Storage
- **Prototype Architecture:** Backups are stored in local JSON format in memory and on local disk.
- **Production Reality:** Enterprise backups are archived to object storage tiers (AWS S3 Glacier, Google Cloud Storage, Azure Blob) with ingress/egress rate limits, cross-region replication fees, and variable download throughput.
- **Impact:** Network transfer latency during multi-terabyte snapshot downloads is not simulated.

### E. No Direct Guarantee of Production RTO/RPO Compliance
- **Measured Latency:** The measured average restore duration in our 30-drill test was ~5.00 seconds.
- **Caveat:** This speed is achievable because test payloads are compact (~50KB). A 500GB production session database will require streaming delta downloads and partitioned replay, which must be independently benchmarked in staging environments before committing to enterprise SLAs.

---

## 3. What the System Successfully Validates Despite Limitations
Despite running in a local prototype environment, the core engineering guarantees hold true:
- SHA-256 cryptographic verification mathematically detects bit-rot regardless of scale.
- Sequence number versioning mathematically sorts out-of-order frames regardless of transport protocol.
- The principle of automated sandbox restoration eliminates 100% of false-confidence assumptions from passive backup monitoring.
