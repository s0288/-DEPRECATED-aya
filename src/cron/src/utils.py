"""
helper funcs for cron job executions
"""

import os
from sqlalchemy import create_engine

def postgres_engine():
    """
    return engine for postgres
    """
    url = f"postgresql://{os.environ.get('AYA_TRACKER_DB_USER')}:"
    url += f"{os.environ.get('AYA_TRACKER_DB_PW')}@{os.environ.get('AYA_TRACKER_DB_HOST')}:"
    url += f"{os.environ.get('AYA_TRACKER_DB_PORT')}/{os.environ.get('AYA_TRACKER_DB_DB')}"
    engine = create_engine(url)
    return engine
