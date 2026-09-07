# RISK REGISTER

| Risk | Likelihood | Impact | Mitigation | Status |
|------|------------|--------|------------|--------|
| **False confidence from successful backup creation** | High | Critical | Do not assume readiness based on backup creation status alone. Require end-to-end restore drills. | Active |
| **Corrupted backup** | Medium | Critical | Implement SHA-256 checksum hashing and verification during restore drills. | Mitigated |
| **Incomplete state restoration** | Low | High | Compare original active state records to the restored dataset. Fail the drill on any divergence. | Mitigated |
| **Incorrect event ordering** | Medium | High | Rely on monotonically increasing `event_version` rather than pure ingest time. | Mitigated |
| **Duplicate event processing** | High | Medium | Enforce idempotency during restore; track `seen_event_ids`. | Mitigated |
| **Unrealistic test data** | Medium | Low | Ensure the session simulator mirrors production complexity (lists, nested JSON state). | Active |
| **Restore test accidentally affecting production** | Low | Critical | Isolate the restore engine strictly in memory or dedicated test tables. | Mitigated |
| **Incorrect RTO/RPO measurement** | Low | Medium | Use strict UTC timestamps and standardized delta calculations. | Mitigated |
