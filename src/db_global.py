#!/usr/bin/python3.6
# coding: utf8

####  --------------------- create tables  ####
## purpose: 
# - class that executes actions from rasa into database (e.g. start events such as fasts)

####  --------------------- event class ####
## purpose: 
# - set up relevant databases
# - add user globally

import os
from sqlalchemy import *

import random
import string
from sqlalchemy.exc import IntegrityError


## add global user (cross-platform) - important: unique slug
## this message is triggered as a custom action when a user sends the first message to the bot
def add_user(created_at, platform_user_id, platform_name, is_bot, received_at):
    N = 8 # unique 8-digit slug, e.g. 7fj41o
    slug = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(N))
    
    stmt = 'INSERT INTO users (slug, created_at, platform_user_id, platform_name, is_bot, received_at) VALUES (%s, %s, %s, %s, %s, %s)'
    args = [slug, created_at, platform_user_id, platform_name, is_bot, received_at]
    
    try:
        conn.execute(stmt, args)
    except IntegrityError as e:
        ## if the slug (the primary key) is the offending column, repeat until the generated slug is accepted
        if "users_pkey" in e.orig.args[0]:
            add_user(created_at, platform_user_id, platform_name, is_bot, received_at)
        ## if the platform_user_id is the offending column, log it
        else:
            print(e)
            ## LOG HERE !!!
    except Exception as e:
        print(e)
        ## LOG HERE !!!





if __name__ == '__main__':
    
    from sqlalchemy import *
    import datetime
    
    engine = create_engine(os.environ["POSTGRES"])
    metadata = MetaData(engine)
    conn = engine.connect()
    
    ## check if databases have been created already
    setup(conn)
    
    ## check if possible to add user
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    received_at = created_at
    platform_user_id = ''.join(random.SystemRandom().choice(string.digits) for _ in range(8))
    platform_name = 'Telegram'
    is_bot = False
    #_
    add_user(created_at, platform_user_id, platform_name, is_bot, received_at)