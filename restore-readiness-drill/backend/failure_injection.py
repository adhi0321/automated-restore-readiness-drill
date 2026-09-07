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
