'''

To make sure that bugs or errors are caught early, an alerting system is required to inform about system activity. 
Uptime_Bot triggers msgs to the Flask app to trigger Telegram msgs to the root user. 

'''

import os
import logging
import crython
import requests
import pandas as pd
from sqlalchemy import create_engine

@crython.job(expr='@daily', root_user=os.environ.get("ROOT_USER"), flask_url=os.environ.get("FLASK_URL"))
def is_active(root_user, flask_url):
    '''
    When Uptime_Bot is initialised, trigger a msg.
    '''
    logging.info(f"starting job: is_active")
    url = flask_url

    try:
        engine = _create_engine()
        interval = '8 days'
        data_users = _get_new_users_in_interval(engine, interval)
        txt = f"interval: last {interval}\n"
        txt += f"- cnt users: {len(data_users)}\n"
        txt += f"- new users: {len(data_users[data_users.new_user_in_interval])}\n"
        txt += f"- currently fasting: {len(data_users[data_users.currently_fasting])}"
        data = {"recipient_id":root_user,"text":txt}
        requests.post(url, json=data)
    except Exception as e: 
        logging.info(f"exception in job: {e}")

def _create_engine():
    url = f"postgresql://{os.environ.get('AYA_TRACKER_DB_USER')}:"
    url += f"{os.environ.get('AYA_TRACKER_DB_PW')}@{os.environ.get('AYA_TRACKER_DB_HOST')}:"
    url += f"{os.environ.get('AYA_TRACKER_DB_PORT')}/{os.environ.get('AYA_TRACKER_DB_DB')}"
    engine = create_engine(url)
    return engine

def _get_new_users_in_interval(engine, interval='8 days'):
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

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
    crython.start()
    crython.join()  ## This will block
