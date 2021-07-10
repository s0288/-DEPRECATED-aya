"""
Report key stats to root user 
"""

import logging
import pandas as pd
import requests


def is_active(root_user, flask_url, engine):
    '''
    When Uptime_Bot is initialised, trigger a msg.
    '''
    logging.info("starting job: is_active")
    url = flask_url

    try:
        interval = '8 days'
        data_users = _get_new_users_in_interval(engine, interval)
        txt = f"interval: last {interval}\n"
        txt += f"- cnt users: {len(data_users)}\n"
        txt += f"- new users: {len(data_users[data_users['new_user_in_interval']])}\n"
        txt += f"- currently fasting: {len(data_users[data_users['currently_fasting']])}"
        data = {"recipient_id":root_user,"text":txt}
        requests.post(url, json=data)
    except Exception as e: 
        logging.info("exception in job: %s", e)

def _get_new_users_in_interval(engine, interval='7 days'):
    """
    Retrieve new users and currently fasting users in interval
    """
    with engine.connect() as con:
        data = pd.read_sql_query(f"""
            select 
                sender_id, 
                case 
                    when min(to_timestamp(timestamp)::date) 
                        > current_date - interval '{interval}'
                        then True
                    else False 
                    end as new_user_in_interval,
                -- CAVEAT: the below query ignores first time fasters
                case
                    when max(timestamp) filter(where action_name = 'action_start_fast')
                        > max(timestamp) filter(where action_name = 'action_end_fast')
                        then True
                    else False
                    end as currently_fasting
            from events 
            group by sender_id
            """, con)
    return data
