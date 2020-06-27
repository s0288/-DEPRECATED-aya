#!/usr/bin/python3.6
# coding: utf8

####  ---------------------  ####
## purpose: 
# - data manipulation functions, specifically for telegram

import os
from sqlalchemy import *
import logging

import src.db_setup
import src.db_global


class Telegram_DB:
    def __init__(self):
        engine = create_engine(os.environ["POSTGRES"])
        metadata = MetaData(engine)
        self.conn = engine.connect()
        ## check if databases have been created already
        src.db_setup(self.conn)

    def add_message(self, message_id, created_at, message, user_id, chat_id, chat_type, bot_command, received_at):
        stmt = 'INSERT INTO telegram (message_id, created_at, message, user_id, chat_id, chat_type, bot_command, received_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        args = [message_id, created_at, message, user_id, chat_id, chat_type, bot_command, received_at]
        try:
            self.conn.execute(stmt, args)
        except Exception as e:
            logging.exception("Exception: Could not write add_message into db")