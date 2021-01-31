#!/usr/bin/python3.6
# coding: utf8

'''

show the most recent chatbot interactions

'''
from sqlalchemy import create_engine
from decouple import config
import pandas as pd

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
                to_timestamp(timestamp) as created_at, 
                id, sender_id, type_name, 
                data::json->'text' as chat_text
            from events 
            where 
                (data::json->'text') is not null
                and to_timestamp(timestamp) > current_date - interval '8 days'
            order by timestamp desc 
            """, con)
    return data

def print_conversation_log(data):
    data = data.iloc[::-1] # reverse order with .iloc[::-1]
    print(f"user_id: {data.sender_id.unique()[0]}", file=open('logs/conversation_log.txt', 'a'))

    for row in data.iterrows():
        if row[1]['type_name'] == 'user':
            print(f"    User: {row[1]['chat_text']}\n", file=open('logs/conversation_log.txt', 'a'))
        else:
            print(f"    Bot: {row[1]['chat_text']}\n", file=open('logs/conversation_log.txt', 'a'))

if __name__ == '__main__':
    engine = create_engine_()
    data = call_db()

    [print_conversation_log(data[data.sender_id == i]) for i in data.sender_id.unique()]
    