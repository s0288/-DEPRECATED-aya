#!/usr/bin/python3.6
# coding: utf8

####  ---------------------  ####
## purpose: 
# - maintain AYA alive on Telegram
## structure:
# - there are 3 key blocks: extracting incoming (extract_main), get outgoing (call_webhook), send outgoing (sent to webhook - NOT in this file)

import time
import logging
import sys

import telegram_bot
import src.call_webhook

def main(chat_id=None):
    # last_update_id is used to make sure that messages are only retrieved once
    last_update_id = None

    while True:
        try:
            logging.info('Hi!')
            
            ##### listen for new messages
            updates = Telegram_Bot.get_updates(last_update_id)
            ## main job
            
            if len(updates["result"]) > 0:
                last_update_id = Telegram_Bot.get_last_update_id(updates) + 1
                # extract incoming message
                chat_id, message = Telegram_Bot.extract_main(updates)
                # get outgoing message
                src.call_webhook(chat_id, message)
        except Exception as e:
            logging.exception(e)

        time.sleep(0.5)
        sys.stdout.write('.'); sys.stdout.flush()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # filename='aya.log'
    Telegram_Bot = telegram_bot.Telegram_Bot()
    main()
