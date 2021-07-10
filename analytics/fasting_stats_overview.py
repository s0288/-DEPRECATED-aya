#!/usr/bin/python3.6
# coding: utf8

'''

give a simple overview of fasting stats

'''
import pandas as pd

from utils import postgres_engine, fasting_stats

def get_events_from_last_n_days(engine, last_n_days=7):
    """
    retrieve events from db
    """
    with engine.connect() as con:
        data = pd.read_sql_query(f"""
            select 
                id, sender_id, to_timestamp(timestamp) as created_at, data::json
            from events 
            where now() - to_timestamp(timestamp) < interval '{last_n_days} days'
            """, con)
    return data

def _create_fasting_text(total_hours, avg_hours, max_hours, last_n_days=7):
    """
    return txt for print stmt
    """
    txt = f"Hier ist deine Übersicht der letzten {last_n_days} Tage:\n"
    txt += f"   {total_hours:,.2f} Stunden insgesamt gefastet\n"
    txt += f"   {avg_hours:,.2f} Stunden durchschnittlich gefastet\n"
    txt += f"   {max_hours:,.2f} Stunden längstes Fasten\n"
    return txt

if __name__ == '__main__':
    engine = postgres_engine()
    LAST_N_DAYS = 7
    df = get_events_from_last_n_days(engine, LAST_N_DAYS)

    for sender_id in df["sender_id"].unique():
        total_hours_fasted, avg_fasted, max_fasted = \
            fasting_stats(df[df["sender_id"] == sender_id].data)
        txt = _create_fasting_text(total_hours_fasted, avg_fasted, max_fasted, LAST_N_DAYS)
        print(sender_id)
        print(txt)
