#!/usr/bin/python3.6
# coding: utf8

'''

give a simple overview of fasting stats

'''
import pandas as pd

from utils import create_engine_
from rasa.actions import ActionSendFastingLog

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
    
    


