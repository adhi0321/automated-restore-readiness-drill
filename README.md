# Automated Restore-Readiness Drill (v0.70 Milestone)

## Project Overview
This project delivers an automated restore-readiness drill engine for a high-velocity multiplayer session-state system. While traditional disaster recovery systems report that backups "completed successfully" (exit code 0 / status 200), actual restoration viability is rarely verified prior to an outage. 

The v0.70 milestone brings the project to approximately **70% completion**, advancing from a basic single-stream prototype into a multi-cluster, cryptographic state verification platform with continuous automated drill execution, full WAL replay, 9 failure injection scenarios, and compliance reporting.

## Key Capabilities (70% Milestone)
- **Multi-Lobby World Simulation**: Concurrent multiplayer session tracking across 4 game modes (Battle Royale 50v50, Dungeon Raid Co-op, Cyber Nexus 5v5 Arena, and Fortress Siege) with live player coordinates, inventories, health, and tick rates.
- **Cryptographic State Integrity**: Real SHA-256 state-tree digests computed using Web Crypto API to catch storage bit-rot and partial writes before deployment.
- **WAL Delta Replay & Sequence Sorting**: Replays write-ahead-log events with Lamport sequence sorting to resolve network jitter and deduplicate at-least-once message deliveries.
- **Continuous Automated Drill Daemon**: Automated background drill scheduler running configurable recovery tests with live countdown timers.
- **Empirical SLA Gating**: Dynamic evaluation of Recovery Time Objective (RTO <= 60s) and Recovery Point Objective (RPO <= 30s) with live threshold sliders.
- **Comprehensive Chaos & Failure Suite (9 Scenarios)**:
  1. *Normal Baseline Restore*: Full clean snapshot and WAL replay within SLA bounds.
  2. *Corrupted Backup (Bit-rot)*: Deliberate mutation of player score/inventory; caught by SHA-256 digest check.
  3. *Duplicate Event Flooding*: Replays duplicate packets to test idempotency filter.
  4. *Out-of-Order Packet Delivery*: Shuffled sequence arrivals safely ordered via sequence buffer.
  5. *Delayed Straggler Event*: Stale events older than checkpoint horizon discarded safely.
  6. *Truncated WAL (Server Crash)*: Simulates server crash mid-write; recovers cleanly up to last uncorrupted frame.
  7. *RTO SLA Threshold Breach*: Simulates storage I/O bottleneck causing recovery time to breach 60s target.
  8. *RPO SLA Threshold Breach*: Simulates cron scheduler stall causing data staleness to exceed 30s limit.
  9. *Concurrent Mutation Conflict*: Simultaneous player loot claims detected via state divergence audit.
- **Dual-Audience Diagnostic Reporting**:
  - *Non-Specialist Recommendations*: Plain-English summaries written for game producers and studio executives.
  - *SRE Root-Cause Analysis*: Technical diagnostics and actionable remediation commands for DevOps engineers.
- **SOC2 / ISO 27001 Compliance Certificate**: Ready-to-export formal disaster recovery evidence with printable PDF formatting and JSON/Markdown export.

## Technology Stack
- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript 5.9+
- **Styling**: Tailwind CSS (High-Density Dark Technical Design Theme)
- **Icons**: Lucide React
- **Cryptography**: Web Crypto API (`crypto.subtle.digest` SHA-256)
- **Architecture**: Self-contained Client Component SPA designed for zero-config, immediate preview compatibility in Google AI Studio without external server dependencies.

## Comparative Evaluation: Baseline vs. 70% Prototype
| Dimension | Traditional Baseline Backup | 70% Restore-Readiness Drill Engine |
|---|---|---|
| **Restore Verification** | Untested until production disaster | Automated continuous sandbox restoration |
| **Cryptographic Checksums** | Missing or file-size only | SHA-256 state tree digest verification |
| **Event Replay** | Blind copy without reordering | Monotonic sequence sorting & deduplication |
| **SLA Measurement** | Theoretical estimates | Empirical timing calculation with strict threshold gates |
| **Chaos Scenarios** | 0 (Happy-path assumptions) | 9 Active Chaos Scenarios |
| **Auditing & Reporting** | Scouring terminal logs | Instant JSON/Markdown export & compliance certificate |

## Running the Application
1. Install dependencies:
   ```bash
   npm install
   ```
2. Run the development server:
   ```bash
   npm run dev
   ```
3. Open [http://localhost:3000](http://localhost:3000) in your browser.

