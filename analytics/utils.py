"""
Helper functions
"""

from decouple import config
from sqlalchemy import create_engine

AYA_TRACKER_DB_HOST = config('AYA_TRACKER_DB_HOST')
AYA_TRACKER_DB_DB = config('AYA_TRACKER_DB_DB')
AYA_TRACKER_DB_USER = config('AYA_TRACKER_DB_USER')
AYA_TRACKER_DB_PW = config('AYA_TRACKER_DB_PW')
AYA_TRACKER_DB_PORT = config('AYA_TRACKER_DB_PORT')

def postgres_engine():
    """
    return engine for postgres
    """
    url = f"postgresql://{AYA_TRACKER_DB_USER}:"
    url += f"{AYA_TRACKER_DB_PW}@{AYA_TRACKER_DB_HOST}:{AYA_TRACKER_DB_PORT}/"
    url += f"{AYA_TRACKER_DB_DB}"
    engine = create_engine(url)
    return engine

def fasting_stats(events):
    """
    derive simple fasting stats
    """
    fasting_log = [event["value"] for event in events \
        if event["event"] == "slot" and event["name"] == "total_hours_fasted"]
    total_hours_fasted = sum(fasting_log)
    avg_fasted = sum(fasting_log) / len(fasting_log)
    max_fasted = max(fasting_log)
    return total_hours_fasted, avg_fasted, max_fasted
