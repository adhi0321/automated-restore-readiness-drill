import os

class Config:
    # Target Metrics
    RTO_TARGET_SECONDS = 60
    RPO_TARGET_SECONDS = 30
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "data", "drill_results.db")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # Ensure data dir exists
    os.makedirs(DATA_DIR, exist_ok=True)
