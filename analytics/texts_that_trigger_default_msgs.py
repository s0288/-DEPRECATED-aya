"""

Create a log of text msgs that triggered default error msgs by Aya.
--> Get list of dialogue break points

"""

import json
import pandas as pd

from utils import postgres_engine
ENGINE = postgres_engine()


def _get_msgs_that_trigger_fallback(engine, interval='7 days'):
    """
    Retrieve msgs that result in fallback
    """
    with engine.connect() as con:
        data = pd.read_sql_query(f"""
            select 
                to_timestamp(timestamp) as timestamp,
                sender_id,
                data::json->>'text' as user_msg,
                data::json->'parse_data'->>'intent_ranking' as intent_ranking
            from events 
            where 
                intent_name = 'nlu_fallback'
                and to_timestamp(timestamp)::date > current_date - interval '{interval}'
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
    fallback_triggers = _get_msgs_that_trigger_fallback(ENGINE)
    for row in fallback_triggers.iterrows():
        print(row[1]["timestamp"], row[1]["sender_id"], row[1]["user_msg"], row[1]["max_intent"])
