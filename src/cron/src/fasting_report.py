"""
create fasting report cronjob for users
"""

import logging
import pandas as pd
import requests


def fasting_report(flask_url, engine, last_n_days=7):
    """
    Provide a regular fasting report to active users
    """
    logging.info("starting job: fasting_report")
    url = flask_url
    try:
        df_events = _get_events_from_last_n_days(engine, last_n_days)

        for sender_id in df_events["sender_id"].unique():
            total_hours_fasted, avg_fasted, max_fasted = _fasting_stats(df_events[df_events["sender_id"] == sender_id].data)
            txt = _create_fasting_text(total_hours_fasted, avg_fasted, max_fasted, last_n_days)
            data = {"recipient_id":sender_id,"text":txt}
            requests.post(url, json=data)
    except Exception as e: 
        logging.info("exception in job: %s", e)

def _get_events_from_last_n_days(engine, last_n_days=7):
    """
    retrieve events for the last n days from db
    """
    with engine.connect() as con:
        data = pd.read_sql_query(f"""
            select 
                id, sender_id, to_timestamp(timestamp) as created_at, data::json
            from events 
            where now() - to_timestamp(timestamp) < interval '{last_n_days} days'
            """, con)
    return data

def _fasting_stats(events):
    """
    derive simple fasting stats
    """
    fasting_log = [event["value"] for event in events \
        if event["event"] == "slot" and event["name"] == "total_hours_fasted"]
    total_hours_fasted = sum(fasting_log)
    avg_fasted = sum(fasting_log) / len(fasting_log)
    max_fasted = max(fasting_log)
    return total_hours_fasted, avg_fasted, max_fasted

def _create_fasting_text(total_hours, avg_hours, max_hours, last_n_days=7):
    """
    return txt for print stmt
    """
    txt = f"Hier ist deine Übersicht der letzten {last_n_days} Tage:\n"
    txt += f"   {total_hours:,.2f} Stunden insgesamt gefastet\n"
    txt += f"   {avg_hours:,.2f} Stunden durchschnittlich gefastet\n"
    txt += f"   {max_hours:,.2f} Stunden längstes Fasten\n"
    return txt
