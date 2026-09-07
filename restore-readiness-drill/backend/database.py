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
    
    # Metadata about drills
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drill_results (
        drill_id TEXT PRIMARY KEY,
        backup_id TEXT,
        attempt_id TEXT,
        started_at REAL,
        completed_at REAL,
        recovery_time_seconds REAL,
        rto_target REAL,
        rpo_target REAL,
        actual_rto REAL,
        actual_rpo REAL,
        rto_pass INTEGER,
        rpo_pass INTEGER,
        checksum_match INTEGER,
        state_match INTEGER,
        overall_result TEXT,
        recommendation TEXT,
        error_message TEXT
    )
    ''')
    conn.commit()
    conn.close()

def save_drill_result(result_dict: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO drill_results (
        drill_id, backup_id, attempt_id, started_at, completed_at, 
        recovery_time_seconds, rto_target, rpo_target, actual_rto, 
        actual_rpo, rto_pass, rpo_pass, checksum_match, state_match, 
        overall_result, recommendation, error_message
    ) VALUES (
        :drill_id, :backup_id, :attempt_id, :started_at, :completed_at,
        :recovery_time_seconds, :rto_target, :rpo_target, :actual_rto,
        :actual_rpo, :rto_pass, :rpo_pass, :checksum_match, :state_match,
        :overall_result, :recommendation, :error_message
    )
    ''', result_dict)
    conn.commit()
    conn.close()

def get_all_drill_results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM drill_results ORDER BY started_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
