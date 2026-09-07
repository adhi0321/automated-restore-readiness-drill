# BASELINE vs PROTOTYPE

## The Baseline Approach
In standard environments, backup routines run periodically. The "Baseline" relies exclusively on the backup system reporting a "200 OK" status upon completion.
- **Restore Testing:** Manual and infrequent. An engineer typically selects a backup and attempts to extract it to a test database.
- **Validation:** Visual inspection. A quick check to see if the database process starts.
- **Events & Consistency:** No verification of duplicate events or out-of-order data processing.
- **Metrics:** Recovery times are estimated manually.

## The Prototype Approach
This project establishes an automated **Restore-Readiness Drill**. 
It eliminates manual checks by providing isolated, programmatic restoration with mathematical validation.

### Comparison Table

| Metric | Baseline | Prototype |
|--------|----------|-----------|
| Restore completion check | Yes (manual) | Yes (automated) |
| Checksum validation | No | Yes |
| State validation | No | Yes |
| RTO measurement | Partial | Yes |
| RPO measurement | No | Yes |
| Failure injection | No | Yes |
| Duplicate event handling | No | Yes |
| Out-of-order handling | No | Yes |
| Automated result reporting | Limited | Yes |
