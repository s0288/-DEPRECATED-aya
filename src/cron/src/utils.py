"""
helper funcs for cron job executions
"""

import os
from sqlalchemy import create_engine

AYA_TRACKER_DB_HOST = os.environ.get('AYA_TRACKER_DB_HOST')
AYA_TRACKER_DB_DB = os.environ.get('AYA_TRACKER_DB_DB')
AYA_TRACKER_DB_USER = os.environ.get('AYA_TRACKER_DB_USER')
AYA_TRACKER_DB_PW = os.environ.get('AYA_TRACKER_DB_PW')
AYA_TRACKER_DB_PORT = os.environ.get('AYA_TRACKER_DB_PORT')

def postgres_engine():
    """
    return engine for postgres
    """
    url = f"postgres://{AYA_TRACKER_DB_USER}:"
    url += f"{AYA_TRACKER_DB_PW}@{AYA_TRACKER_DB_HOST}:{AYA_TRACKER_DB_PORT}/"
    url += f"{AYA_TRACKER_DB_DB}"
    engine = create_engine(url)
    return engine
