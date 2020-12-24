'''

When fasting, I'd like to get a summary of my fasting progress, e.g. sth like this: 

Hier ist deine Übersicht der letzten 7 Tage:
 - du hast 103 Stunden gefastet
 - deine durchschnittliche Fastenzeit betrug 15 Stunden und 17 Minuten
 - deine längste Fastenzeit war 16 Stunden und 38 Minuten

'''
from sqlalchemy import  create_engine
from decouple import config
import pandas as pd

AYA_TRACKER_DB_HOST = config('AYA_TRACKER_DB_HOST')
AYA_TRACKER_DB_DB = config('AYA_TRACKER_DB_DB')
AYA_TRACKER_DB_USER = config('AYA_TRACKER_DB_USER')
AYA_TRACKER_DB_PW = config('AYA_TRACKER_DB_PW')
AYA_TRACKER_DB_PORT = config('AYA_TRACKER_DB_PORT')
ROOT_USER = config('ROOT_USER')
engine = create_engine(f"postgres://{AYA_TRACKER_DB_USER}:{AYA_TRACKER_DB_PW}@{AYA_TRACKER_DB_HOST}:{AYA_TRACKER_DB_PORT}/{AYA_TRACKER_DB_DB}")

if __name__ == '__main__':
    with engine.connect() as con:
        data = pd.read_sql_query("""
            select 
                id, sender_id, timestamp, action_name, data::json ->> 'value' as total_hours_fasted
            from events 
            where action_name = 'total_hours_fasted'
            order by id desc 
            """, con)

    data["created_at"] = pd.to_datetime(data.timestamp, unit='s')

data.head()

def get_fasting_log(data):
    '''
    Provide a fasting summary to the user, e.g.:
        Hier ist deine Übersicht der letzten 7 Tage:
            - du hast 103 Stunden gefastet
            - deine durchschnittliche Fastenzeit betrug 15 Stunden und 17 Minuten
            - deine längste Fastenzeit war 16 Stunden und 38 Minuten

    Parameters:
        data (dataframe): total_hours_fasted event data from user with sender_id X

    Returns:
        total_fasted_7d: float; total time fasted during prev. 7 days    
        avg_fasted_7d: float; avg time fasted during prev. 7 days
        max_fasted_7d: float; max time fasted during prev. 7 days
    '''
    total_fasted_7d = data.total_hours_fasted.astype(float).sum()
    avg_fasted_7d = data.total_hours_fasted.astype(float).mean()
    max_fasted_7d = data.total_hours_fasted.astype(float).max()

    return total_fasted_7d, avg_fasted_7d, max_fasted_7d

total_fasted_7d, avg_fasted_7d, max_fasted_7d = get_fasting_log(data[data.sender_id==ROOT_USER])

print(f"Hier ist deine Übersicht der letzten 7 Tage:\n    - du hast insgesamt {total_fasted_7d:,.2f} Stunden gefastet\n    - du hast durchschn. {avg_fasted_7d:,.2f} Stunden gefastet\n    - deine längste Fastendauer betrug {max_fasted_7d:,.2f} Stunden")