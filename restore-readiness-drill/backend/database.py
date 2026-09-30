import sqlite3
import json
from .config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table if not exists with base primary key
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drill_results (
        drill_id TEXT PRIMARY KEY
    )
    ''')
    
    cursor.execute("PRAGMA table_info(drill_results)")
    existing_cols = {row["name"] for row in cursor.fetchall()}
    
    needed_cols = [
        ("scenario", "TEXT"),
        ("backup_id", "TEXT"),
        ("session_id", "TEXT"),
        ("attempt_id", "TEXT"),
        ("start_time", "REAL"),
        ("end_time", "REAL"),
        ("started_at", "REAL"),
        ("completed_at", "REAL"),
        ("recovery_time", "REAL"),
        ("recovery_time_seconds", "REAL"),
        ("rto_target", "REAL"),
        ("actual_rto", "REAL"),
        ("rto_pass", "INTEGER"),
        ("rpo_target", "REAL"),
        ("actual_rpo", "REAL"),
        ("rpo_pass", "INTEGER"),
        ("checksum_match", "INTEGER"),
        ("checksum_result", "TEXT"),
        ("state_match", "INTEGER"),
        ("state_validation_result", "TEXT"),
        ("state_integrity_result", "TEXT"),
        ("overall_result", "TEXT"),
        ("error_reason", "TEXT"),
        ("error_message", "TEXT"),
        ("recommendation", "TEXT")
    ]
    for col_name, col_type in needed_cols:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE drill_results ADD COLUMN {col_name} {col_type}")
            
    conn.commit()
    conn.close()


def save_drill_result(result_dict: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fill defaults if missing
    record = {
        "drill_id": result_dict.get("drill_id", ""),
        "scenario": result_dict.get("scenario", "NORMAL"),
        "backup_id": result_dict.get("backup_id", ""),
        "session_id": result_dict.get("session_id", "session_1"),
        "attempt_id": result_dict.get("attempt_id", ""),
        "start_time": result_dict.get("start_time", result_dict.get("started_at", 0.0)),
        "end_time": result_dict.get("end_time", result_dict.get("completed_at", 0.0)),
        "started_at": result_dict.get("started_at", result_dict.get("start_time", 0.0)),
        "completed_at": result_dict.get("completed_at", result_dict.get("end_time", 0.0)),
        "recovery_time": result_dict.get("recovery_time", result_dict.get("recovery_time_seconds", 0.0)),
        "recovery_time_seconds": result_dict.get("recovery_time_seconds", result_dict.get("recovery_time", 0.0)),
        "rto_target": result_dict.get("rto_target", 60.0),
        "actual_rto": result_dict.get("actual_rto", 0.0),
        "rto_pass": int(result_dict.get("rto_pass", 0)),
        "rpo_target": result_dict.get("rpo_target", 30.0),
        "actual_rpo": result_dict.get("actual_rpo", 0.0),
        "rpo_pass": int(result_dict.get("rpo_pass", 0)),
        "checksum_match": int(result_dict.get("checksum_match", 0)),
        "checksum_result": result_dict.get("checksum_result", "PASS" if result_dict.get("checksum_match") else "FAIL"),
        "state_match": int(result_dict.get("state_match", 0)),
        "state_validation_result": result_dict.get("state_validation_result", "PASS" if result_dict.get("state_match") else "FAIL"),
        "state_integrity_result": result_dict.get("state_integrity_result", "PASS" if result_dict.get("state_match") else "FAIL"),
        "overall_result": result_dict.get("overall_result", "FAIL"),
        "error_reason": result_dict.get("error_reason", result_dict.get("error_message", "")),
        "error_message": result_dict.get("error_message", result_dict.get("error_reason", "")),
        "recommendation": result_dict.get("recommendation", "")
    }

    cursor.execute('''
    INSERT OR REPLACE INTO drill_results (
        drill_id, scenario, backup_id, session_id, attempt_id,
        start_time, end_time, started_at, completed_at,
        recovery_time, recovery_time_seconds,
        rto_target, actual_rto, rto_pass,
        rpo_target, actual_rpo, rpo_pass,
        checksum_match, checksum_result,
        state_match, state_validation_result, state_integrity_result,
        overall_result, error_reason, error_message, recommendation
    ) VALUES (
        :drill_id, :scenario, :backup_id, :session_id, :attempt_id,
        :start_time, :end_time, :started_at, :completed_at,
        :recovery_time, :recovery_time_seconds,
        :rto_target, :actual_rto, :rto_pass,
        :rpo_target, :actual_rpo, :rpo_pass,
        :checksum_match, :checksum_result,
        :state_match, :state_validation_result, :state_integrity_result,
        :overall_result, :error_reason, :error_message, :recommendation
    )
    ''', record)
    conn.commit()
    conn.close()


def get_all_drill_results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM drill_results ORDER BY started_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
