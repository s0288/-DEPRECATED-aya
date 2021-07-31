"""

Create a log of text msgs that triggered default error msgs by Aya.
--> Get list of dialogue break points

"""

import json
import pandas as pd

from utils import postgres_engine
ENGINE = postgres_engine()

def _get_msgs_that_trigger_fallback(engine, fallback_type="nlu", interval='7 days'):
    """
    Retrieve msgs that result in fallback
    """
    if fallback_type=="nlu":
        id_condition = """
            select id as fallback_msg_id from events
            where intent_name = 'nlu_fallback'
            """
    elif fallback_type=='action':
        id_condition = """
            select 
                (
                    select min(id)
                    from events e2
                    where e2.id > e1.id and type_name='user'
                ) as fallback_msg_id
            from events e1
            where 
                data::json->'metadata'->>'template_name' = 'utter_default'
            """

    with engine.connect() as con:
        data = pd.read_sql_query(f"""
            with ids as (
                {id_condition}
            )
            select 
                to_timestamp(timestamp) as timestamp,
                id, 
                sender_id,
                data::json->>'text' as user_msg,
                data::json->'parse_data'->>'intent_ranking' as intent_ranking
            from events e
            join ids i
                on e.id = i.fallback_msg_id
            where
                to_timestamp(timestamp)::date > current_date - interval '{interval}'
            order by timestamp desc
            """, con)
    data["max_intent"] = data["intent_ranking"].apply(lambda x: _extract_top_intent(json.loads(x)))
    data = data.drop("intent_ranking", axis=1)
    return data

def _extract_top_intent(intent_ranking):
    max_confidence = max([row["confidence"] for row in intent_ranking])
    max_intent = [[row["name"], v] for row in intent_ranking \
        for k, v in row.items() if v == max_confidence][0]
    return max_intent


if __name__ == '__main__':
    print("nlu fallbacks:")
    print(_get_msgs_that_trigger_fallback(ENGINE, fallback_type='nlu'))
    print("\n------\n")
    print("action fallbacks:")
    print(_get_msgs_that_trigger_fallback(ENGINE, fallback_type='action'))