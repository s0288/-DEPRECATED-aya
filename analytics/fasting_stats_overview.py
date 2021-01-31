#!/usr/bin/python3.6
# coding: utf8

'''

give a simple overview of fasting stats

'''
from sqlalchemy import create_engine
from decouple import config
import pandas as pd

from rasa.actions import ActionSendFastingLog

def create_engine_():
    AYA_TRACKER_DB_HOST = config('AYA_TRACKER_DB_HOST')
    AYA_TRACKER_DB_DB = config('AYA_TRACKER_DB_DB')
    AYA_TRACKER_DB_USER = config('AYA_TRACKER_DB_USER')
    AYA_TRACKER_DB_PW = config('AYA_TRACKER_DB_PW')
    AYA_TRACKER_DB_PORT = config('AYA_TRACKER_DB_PORT')
    engine = create_engine(f"postgres://{AYA_TRACKER_DB_USER}:{AYA_TRACKER_DB_PW}@{AYA_TRACKER_DB_HOST}:{AYA_TRACKER_DB_PORT}/{AYA_TRACKER_DB_DB}")
    return engine


def call_db():
    with engine.connect() as con:
        data = pd.read_sql_query("""
            select 
                id, sender_id, to_timestamp(timestamp) as created_at, data::json
            from events 
            """, con)
    return data

def fasting_stats(user, events):
    fasting_stats_ = ActionSendFastingLog.retrieve_fasting_log(events)
    print(f"User {user}: \n  gefastet insgesamt: {fasting_stats_[2]:,.2f} Stunden \n  durchschnittlich gefastet: {fasting_stats_[3]:,.2f} Stunden \n  längstes Fasten: {fasting_stats_[4]:,.2f} Stunden \n  fastet seit: {fasting_stats_[0]:,} Tagen")
    print("")

if __name__ == '__main__':
    engine = create_engine_()
    data = call_db()
    
    [fasting_stats(i, data[data.sender_id == i].data) for i in data.sender_id.unique()]
    
    


