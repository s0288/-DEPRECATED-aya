"""
Add Cron jobs based on user stats
"""
import pandas as pd

from utils import create_engine_

def _get_new_users_in_interval(interval='8 days'):
    with engine.connect() as con:
        data = pd.read_sql_query(f"""
            select 
                sender_id, 
                count(*) 
                    filter(where to_timestamp(timestamp) > current_date - interval '8 days'
                        and type_name = 'user') 
                    as cnt_msgs,
                min(to_timestamp(timestamp)::date) as first_interaction,
                case 
                    when min(to_timestamp(timestamp)::date) 
                        > current_date - interval '8 days'
                        then True
                    else False 
                    end as new_user_in_interval,
                -- CAVEAT: the below query ignores first time fasters
                case
                    when max(timestamp) filter(where action_name = 'action_start_fast')
                        > max(timestamp) filter(where action_name = 'action_end_fast')
                        then True
                    else False
                    end as currently_fasting,
                max(timestamp) filter(where action_name = 'action_start_fast') as start_fast,
                max(timestamp) filter(where action_name = 'action_end_fast') as end_fast
            from events 
            group by sender_id
            """, con)
    return data

if __name__ == '__main__':
    engine = create_engine_()
    interval = '8 days'
    data = _get_new_users_in_interval(interval)
    txt = f"interval: last {interval}\n"
    txt += f"- cnt users: {len(data)}\n"
    txt += f"- new users: {len(data[data.new_user_in_interval])}\n"
    txt += f"- currently fasting: {len(data[data.currently_fasting])}"
    
    print(txt)
    print(data)