"""
Helper functions
"""

from decouple import config
from sqlalchemy import create_engine

def create_engine_():
    AYA_TRACKER_DB_HOST = config('AYA_TRACKER_DB_HOST')
    AYA_TRACKER_DB_DB = config('AYA_TRACKER_DB_DB')
    AYA_TRACKER_DB_USER = config('AYA_TRACKER_DB_USER')
    AYA_TRACKER_DB_PW = config('AYA_TRACKER_DB_PW')
    AYA_TRACKER_DB_PORT = config('AYA_TRACKER_DB_PORT')
    engine = create_engine(f"postgres://{AYA_TRACKER_DB_USER}:{AYA_TRACKER_DB_PW}@{AYA_TRACKER_DB_HOST}:{AYA_TRACKER_DB_PORT}/{AYA_TRACKER_DB_DB}")
    return engine
