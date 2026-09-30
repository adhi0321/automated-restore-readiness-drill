import random
import copy
from .models import BackupData

def inject_corrupted_backup(backup: BackupData) -> BackupData:
    """Modifies payload without updating checksum to simulate bit rot/corruption."""
    corrupted_backup = copy.deepcopy(backup)
    if corrupted_backup.events:
        corrupted_backup.events[0].payload["score"] = -9999
    return corrupted_backup

def inject_duplicate_event(backup: BackupData) -> BackupData:
    """Adds an exact duplicate of an existing event."""
    duped_backup = copy.deepcopy(backup)
    if duped_backup.events:
        duped_event = copy.deepcopy(duped_backup.events[-1])
        duped_backup.events.append(duped_event)
        # Fix checksum so it's a valid backup technically, but has dupes
        from .backup_service import generate_checksum
        backup_json = duped_backup.model_dump_json(exclude={"checksum"})
        duped_backup.checksum = generate_checksum(backup_json)
    return duped_backup

def inject_out_of_order_events(backup: BackupData) -> BackupData:
    """Shuffles the events."""
    ooo_backup = copy.deepcopy(backup)
    random.shuffle(ooo_backup.events)
    # Fix checksum
    from .backup_service import generate_checksum
    backup_json = ooo_backup.model_dump_json(exclude={"checksum"})
    ooo_backup.checksum = generate_checksum(backup_json)
    return ooo_backup

def inject_delayed_event(backup: BackupData) -> BackupData:
    """Simulates an event with an older timestamp that arrived at the end."""
    delayed_backup = copy.deepcopy(backup)
    if len(delayed_backup.events) > 1:
        # Take the first event and append it to the end (but give it a new ID so it's treated as a late-arriving old-version event)
        late_event = copy.deepcopy(delayed_backup.events[0])
        late_event.event_id = "delayed-" + late_event.event_id
        # Version is old, but it's positioned at the end of the log
        delayed_backup.events.append(late_event)
        
        from .backup_service import generate_checksum
        backup_json = delayed_backup.model_dump_json(exclude={"checksum"})
        delayed_backup.checksum = generate_checksum(backup_json)
    return delayed_backup

def inject_truncated_wal(backup: BackupData) -> BackupData:
    """Simulates abrupt crash leaving truncated/partial WAL events."""
    truncated = copy.deepcopy(backup)
    if len(truncated.events) > 2:
        truncated.events = truncated.events[:len(truncated.events) // 2]
    from .backup_service import generate_checksum
    backup_json = truncated.model_dump_json(exclude={"checksum"})
    truncated.checksum = generate_checksum(backup_json)
    return truncated

def inject_concurrent_conflict(backup: BackupData) -> BackupData:
    """Simulates two conflicting mutations on the same key with identical version."""
    conflict_backup = copy.deepcopy(backup)
    if conflict_backup.events:
        conflict_event = copy.deepcopy(conflict_backup.events[-1])
        conflict_event.event_id = "conflict-" + conflict_event.event_id
        conflict_event.payload = {"contested_resource": "PLAYER_B_CLAIM"}
        conflict_backup.events.append(conflict_event)
        from .backup_service import generate_checksum
        backup_json = conflict_backup.model_dump_json(exclude={"checksum"})
        conflict_backup.checksum = generate_checksum(backup_json)
    return conflict_backup

def inject_rto_breach(backup: BackupData) -> BackupData:
    """Simulates storage I/O bottleneck causing restore time to exceed RTO target (60s)."""
    breach_backup = copy.deepcopy(backup)
    setattr(breach_backup, 'simulated_rto_delay', 74.85)
    return breach_backup

def inject_rpo_breach(backup: BackupData, failure_time: float) -> BackupData:
    """Simulates missed snapshot schedule causing data staleness to exceed RPO target (30s)."""
    breach_backup = copy.deepcopy(backup)
    # Set all event timestamps backwards so lag is 85.0s > 30s
    for i, event in enumerate(breach_backup.events):
        event.timestamp = failure_time - 85.0 + (i * 0.1)
    from .backup_service import generate_checksum
    backup_json = breach_backup.model_dump_json(exclude={"checksum"})
    breach_backup.checksum = generate_checksum(backup_json)
    return breach_backup


