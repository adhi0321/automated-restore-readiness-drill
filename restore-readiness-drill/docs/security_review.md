# SECURITY, SAFETY, AND ISOLATION REVIEW

## 1. Security Architecture & Threat Model
The Automated Restore-Readiness Drill engine operates with strict safety controls to prevent two critical disaster recovery risks:
1. **Accidental Production Execution:** A test restore drill inadvertently overwriting live active player sessions.
2. **Corrupted / Tampered Data Ingestion:** Unverified or maliciously modified backup archives executing arbitrary deserialization or polluting datastores.

---

## 2. Security Assessment & Control Matrix

| Security / Safety Domain | Threat / Vulnerability Analyzed | Mitigation Implemented in Prototype | Verification Status |
|:---|:---|:---|:---:|
| **Test-Data Isolation** | Test restore processes writing to or altering production game state tables. | Strict isolation: Drills execute entirely within isolated in-memory objects or dedicated sandbox database tables (`drill_results`). The drill engine has zero write permissions to active game lobbies. | **VERIFIED** |
| **Production Credentials** | Hardcoded API keys, database passwords, or cloud credentials exposed in code. | Zero credentials required. The prototype uses local SQLite (`drill_metadata.db`) and Web Crypto API. No secrets exist in the codebase. `.env.example` provides template variables without secrets. | **VERIFIED** |
| **API Input Validation** | Malicious injection via query parameters (e.g. `POST /api/drills/run?scenario=...`). | FastAPI schema validation with strict string allowlisting (`NORMAL`, `CORRUPTED`, `DUPLICATE`, `OUT_OF_ORDER`, `DELAYED`, `TRUNCATED_WAL`, etc.). Unrecognized inputs fall back safely to `NORMAL`. | **VERIFIED** |
| **SQLite Safety & SQLi** | SQL injection attacks via drill results or metadata fields. | Parameterized queries used exclusively throughout `backend/database.py` (using `:drill_id`, `:scenario`, etc.). No dynamic string interpolation in SQL statements. | **VERIFIED** |
| **Cryptographic Integrity** | Silent bit rot, unauthorized modification, or man-in-the-middle tampering. | SHA-256 state tree digest calculated over canonical JSON bytes (`model_dump_json(exclude={'checksum'})`). Any altered bit triggers immediate rejection before deserialization. | **VERIFIED** |
| **Unsafe File Writes & Traversal** | Path traversal attacks (`../../etc/passwd`) via backup IDs or file exports. | Filenames and export paths are strictly sanitized with `os.path.basename()` and pinned inside dedicated `evidence/` and `data/` directories. No arbitrary path inputs permitted. | **VERIFIED** |
| **Accidental Production Failover**| Drill harness triggering live DNS or matchmaking routing switch. | The drill engine is strictly an observational and validation platform. It possesses no orchestration hooks or network credentials to alter live game load balancers. | **VERIFIED** |
| **Memory Isolation & Leakage** | Memory leaks from uncollected restore attempt objects. | Short-lived function scopes and garbage collection of temporary `BackupData` and `SessionState` objects upon drill completion. | **VERIFIED** |

---

## 3. Sandboxing & Safe Execution Checklist
- [x] All database operations use prepared/parameterized statements.
- [x] Pre-restore checksum verification occurs before any memory deserialization.
- [x] All file operations use sandboxed absolute directories.
- [x] Zero production cloud keys or credentials stored in repository.
- [x] Idempotency logic prevents duplicate transaction processing.
