# DISASTER RECOVERY RISK REGISTER

This risk register incorporates empirical findings, failure frequencies, and mitigation proofs gathered from the 30-drill controlled experiment.

---

## Risk Assessment Matrix

| Risk ID | Risk Description | Likelihood | Impact | Measured Experiment Evidence | Mitigation Implemented | Residual Risk | Status |
|:---|:---|:---:|:---:|:---|:---|:---:|:---:|
| **RSK-001** | **False Confidence from Successful Backups** | High | Critical | Baseline claimed 100% readiness, but 20/30 backups had undetected flaws causing recovery failure. | Automated end-to-end sandbox restore drills before marking backups as ready. | Low | **Mitigated** |
| **RSK-002** | **Silent Storage Bit-Rot / Checksum Mismatch** | Medium | Critical | 3/3 corrupted backups were intercepted at Stage 1 by SHA-256 check before state allocation. | Cryptographic SHA-256 pre-restore integrity verification against signed manifest. | Very Low | **Mitigated** |
| **RSK-003** | **Incomplete State Restoration (Truncated WAL)** | Medium | High | 2/2 truncated WAL drills were detected via sequence gap checks (`restored_v < expected_v`). | Version continuity gating; rollback to last atomic checkpoint with CRC block framing. | Low | **Mitigated** |
| **RSK-004** | **Duplicate Event Processing** | High | High | 3/3 duplicate event drills were deduplicated cleanly with 0 state divergence (100% integrity). | Ingestion idempotency cache (`seen_event_ids` hash set) and sequence deduplication. | Very Low | **Mitigated** |
| **RSK-005** | **Out-of-Order Packet Application** | High | Medium | 3/3 shuffled packet drills were sorted by monotonic version before application (100% match). | Strict sequence-order sorting prior to memory state materialization. | Very Low | **Mitigated** |
| **RSK-006** | **Delayed Straggler Event Rollback** | Medium | Medium | 3/3 delayed event drills were processed without unwinding newer version states. | Lamport sequence gating preventing stale version updates from overwriting current fields. | Very Low | **Mitigated** |
| **RSK-007** | **Recovery Time SLA Breach (RTO > 60s)** | Medium | High | 2/2 slow restore drills (74.85s) were flagged by the SLA gate, preventing false compliance. | Periodic snapshot compaction every 30s; IOPS scaling for restore worker pools. | Medium | **Monitored** |
| **RSK-008** | **Data Staleness SLA Breach (RPO > 30s)** | Medium | High | 2/2 stale backup drills (72.80s lag) were flagged by RPO telemetry monitor. | Continuous WAL stream replication and automated alerting when replication lag > 15s. | Medium | **Monitored** |
| **RSK-009** | **Concurrent Mutation Conflicts** | Low | High | 2/2 concurrent conflict drills were flagged as contested mutations and halted safely. | Enforced Lamport timestamp arbitration and distributed lock consensus at gateway. | Low | **Mitigated** |
| **RSK-010** | **Test Data Scale Limitations** | High | Low | Workload tested 20–40 events per session rather than millions of concurrent players. | Clearly document prototype boundaries; plan cloud load-testing harness for production. | Medium | **Active** |
| **RSK-011** | **Simulation Environment Divergence** | High | Medium | SQLite and in-memory replay do not exhibit distributed network latency or cross-AZ partition. | Clearly label all simulation boundaries; plan distributed Redis/Kafka validation. | Medium | **Active** |

---

## Risk Review Protocol
1. **Weekly Automated Audit:** The drill engine executes scheduled background chaos drills and automatically flags any emerging RTO/RPO regressions into the SQLite telemetry store.
2. **Quarantine Automation:** Any backup triggering `RSK-001`, `RSK-002`, or `RSK-003` is instantly excluded from the active recovery pool, and an alert is broadcast to on-call engineering.
