#!/usr/bin/python3.6
# coding: utf8

####  ---------------------  ####
## purpose: 
# - maintain AYA alive on Telegram
## structure:
# - there are 3 key blocks: extract incoming (extract_main), get outgoing (call_webhook), send outgoing (sent to webhook - NOT in this file)

import time
import logging
import sys
import os

from telegram_listener import Telegram_Listener
from call_rasa import call_rasa

def main(chat_id=None):
    # last_update_id is used to make sure that messages are only retrieved once
    next_update_id = None
    logging.info(f"starting telegram_bot")

    while True:
        try:
            ##### listen for new messages
            update, next_update_id = Telegram_Listener.get_update_and_next_update_id(next_update_id)
            
            if update:
                # extract incoming message
                chat_id, message = Telegram_Listener.extract_main(update)
                logging.info(f"user message: {message}")

                if not all((chat_id, message)):
                    # if a user provides input that is not expected (e.g. adding a user to a chat), ignore these inputs for now
                    # better solution is to set a default "I don't know what this means" response and send it to Rasa
                    continue
                webhook_response = call_rasa(chat_id, message)
                logging.info(f"webhook_response: {webhook_response}")
        except Exception as e:
            logging.exception(e)

        time.sleep(0.5)
        sys.stdout.write('.'); sys.stdout.flush()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO) # filename='aya.log'
    Telegram_Listener = Telegram_Listener()
    main()
