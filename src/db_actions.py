#!/usr/bin/python3.6
# coding: utf8

####  --------------------- create tables  ####
## purpose: 
# - class that executes actions from rasa into database (e.g. start events such as fasts)

####  --------------------- event class ####
## purpose: 
# - add actions to action db


from sqlalchemy import *
import src.config
import logging

#### event class
class Actions_DB:
    def __init__(self):
        engine = create_engine(src.config.POSTGRES)
        metadata = MetaData(engine)
        self.conn = engine.connect()


    ## add an event to db, e.g. "start_fast"
    def add_action(self, name, created_at, platform_user_id, platform_name, value, received_at):
        stmt =  """ 
                INSERT INTO 
                    actions (name, created_at, platform_user_id, platform_name, value, received_at) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
                """
        args = [name, created_at, platform_user_id, platform_name, value, received_at]
        try:
            self.conn.execute(stmt, args)
        except Exception as e:
            logging.exception("Exception: Could not add event to db")


    ## get info if there is an unfinished fast and, if so, when it started
    def get_last_start_fast(self, platform_user_id, platform_name):
        stmt = """ 
                SELECT
                    CASE 
                        WHEN a.name = 'start_fast' THEN a.created_at
                        ELSE Null 
                        END AS fasting_since
                FROM
                    actions a
                WHERE 
                    a.created_at = 
                    (
                    SELECT
                        -- get most recent value
                        max(a.created_at) AS created_at
                    FROM
                        actions a
                    WHERE
                        a.platform_user_id = '%s'
                        and a.name in ('start_fast', 'end_fast')
                    )
                    AND a.platform_user_id = '%s'
             """
        args = [platform_user_id, platform_user_id]
        try:
            return self.conn.execute(stmt, args).fetchall()[0][0]
        except Exception as e:
            logging.exception("Exception: Could not get last start fast from db")