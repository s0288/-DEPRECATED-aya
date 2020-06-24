#!/usr/bin/python3.6
# coding: utf8

####  --------------------- create tables  ####
## purpose: 
# - set up relevant databases


from sqlalchemy import *

##### create tables
## create data tables + indices
def db_setup(conn):
    print("creating non-existent tables ...")
    users_stmt =    """ 
                CREATE TABLE IF NOT EXISTS users 
                    (
                        id serial, 
                        slug text PRIMARY KEY,
                        created_at timestamp, 
                        platform_user_id text UNIQUE, 
                        platform_name text,  
                        is_bot boolean,
                        received_at timestamp
                    ) 
                    """
    
    telegram_stmt = """ 
                CREATE TABLE IF NOT EXISTS telegram 
                    (
                        id serial PRIMARY KEY, 
                        message_id int,
                        created_at timestamp,  
                        message text, 
                        user_id text, 
                        chat_id text, 
                        chat_type text, 
                        bot_command text, 
                        received_at timestamp
                    ) 
                    """

    actions_stmt = """ 
                CREATE TABLE IF NOT EXISTS actions
                    (
                        id serial PRIMARY KEY, 
                        name text,
                        created_at timestamp,  
                        platform_user_id text, 
                        platform_name text,  
                        value text, 
                        received_at timestamp
                    ) 
                    """

    telegramididx = 'CREATE INDEX IF NOT EXISTS idIndex ON telegram (id ASC)'
    userididx = 'CREATE INDEX IF NOT EXISTS idUserIndex ON users (id ASC)'
    actionididx = 'CREATE INDEX IF NOT EXISTS idActions ON actions (id ASC)'
    
    conn.execute(users_stmt)
    conn.execute(telegram_stmt)
    conn.execute(actions_stmt)
    
    conn.execute(telegramididx)
    conn.execute(userididx)
    conn.execute(actionididx)
