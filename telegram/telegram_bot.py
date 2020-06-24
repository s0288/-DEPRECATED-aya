#!/usr/bin/python3.6
# coding: utf8

####  ---------------------  ####
## purpose: 
# - extract functions, save functions and send functions

import requests
import json
import datetime
import urllib
import logging

# from db_bot import Telegram_DB 
import src.db_telegram_bot
import src.call_webhook

import src.config

Telegram_DB = src.db_telegram_bot.Telegram_DB()

URL = f"https://api.telegram.org/bot{src.config.TELEGRAM_TOKEN}/"

class Telegram_Bot:
# ------ save message to db
    # key function to save to database
    def save_message(message_elements):
        # set time when message was saved to db
        message_elements['received_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # save message to db
        try:
            Telegram_DB.add_message(message_elements['message_id'], message_elements['created_at'], message_elements['message'], message_elements['user_id'], message_elements['chat_id'], message_elements['chat_type'], message_elements['bot_command'], message_elements['received_at'])
        except Exception as e:
            logging.exception(e)

# ------ process incoming messages
    def get_json_from_url(url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = URL + "getUpdates?timeout=600"
        if offset:
            url += "&offset={}".format(offset)
        js = Telegram_Bot.get_json_from_url(url)
        return js

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return min(update_ids)

    # for handling inline buttons
    def answer_callback(callback_query_id, text=None):
        url = URL + "answerCallbackQuery?callback_query_id={}".format(callback_query_id)
        if text:
            url += "&text={}".format(text)
        Telegram_Bot.get_json_from_url(url)
# ------ end: process incoming messages

# ------ extract content of incoming messages
    # main extract_ function that defines where an update is routed towards
    def extract_main(self, updates):
        for update in updates["result"]:
            # message container for incoming and outgoing msgs
            message_elements = {'created_at': None, 'received_at': None, 'message_id': None, 
                                'message': None, 'user_id': None, 'chat_id': None, 'bot_command': None, 
                                'img': None, 'is_bot': None, 'callback_query_id': None, 'chat_type': None}

            # check whether we're dealing with a message, a callback or not-to-be-extracted content
            extraction_method = Telegram_Bot.set_extraction_method(update)
            if extraction_method not in ['do_not_extract']:
                if extraction_method == 'extract_message':
                    message_elements = Telegram_Bot.extract_message(message_elements, update['message'])
                elif extraction_method == 'extract_callback':
                    message_elements = Telegram_Bot.extract_callback(message_elements, update['callback_query'])
                
                # save user message to db
                Telegram_Bot.save_message(message_elements)

                # return chat_id and message for handling a reply
                return message_elements["chat_id"], message_elements["message"]

    # invoked in extract_updates() --> decides whether we are dealing with a message, a callback or not-to-be-extracted content
    def set_extraction_method(update):
        extraction_method = None
        # check whether we're dealing with a message or a callback
        if update.get('message') is not None:
            # users can trigger out-of-the-ordinary actions, ignore such cases
            if (update["message"].get('group_chat_created') is None 
                    or update["message"].get('new_chat_participant') is None 
                    or update["message"].get('left_chat_participant') is None):
                extraction_method = 'extract_message'
            # fallback for out-of-the-ordinary actions
            else:
                ## replace print with logging event !!
                logging.info("received a do_not_extract_event")
                extraction_method = 'do_not_extract'
        elif update.get('callback_query') is not None:
            extraction_method = 'extract_callback'
        return extraction_method

    # invoked in extract_updates() - for extracting incoming messages
    def extract_message(message_elements, message):
        # save attributes
        message_elements['created_at'] = datetime.datetime.fromtimestamp(int(message["date"])).strftime('%Y-%m-%d %H:%M:%S.%f')
        message_elements['message_id'] = message["message_id"]
        # if the message has text, save it
        if message.get('text') is not None:
            message_elements['message'] = message["text"]
        # if the user sent a file, e.g. pdf, save it
        elif message.get('document') is not None and message["from"]["is_bot"] is False:
            message_elements['message'] = 'file: ' + message["document"]["file_id"]
        # if the user sent an img, e.g. jpg, save it
        elif message.get('photo') is not None and message["from"]["is_bot"] is False:
            try:
                message_elements['message'] = 'file: ' + message["photo"][3]["file_id"]
            except:
                message_elements['message'] = 'file: ' + message["photo"][0]["file_id"]
        message_elements['user_id'] = message["from"]["id"]
        message_elements['chat_id'] = message["chat"]["id"]
        # if the user sends a bot_command (e.g. /start or /check_in), save it
        if message.get('entities') is not None:
            for entity in message["entities"]:
                message_elements['bot_command'] = entity["type"]
        message_elements['is_bot'] = message["from"]["is_bot"]
        message_elements['chat_type'] = message["chat"]["type"]
        return message_elements

    # invoked in extract_updates() - for extracting inline button presses
    def extract_callback(message_elements, message):
        # save callback_query_id
        message_elements['callback_query_id'] = message["id"]
        # remove loading button on the client
        Telegram_Bot.answer_callback(message_elements['callback_query_id'])
        # save remaining parameters
        message_elements['created_at'] = datetime.datetime.fromtimestamp(int(message["message"]["date"])).strftime('%Y-%m-%d %H:%M:%S.%f')
        message_elements['message_id'] = message["message"]["message_id"]
        message_elements['message'] = message["data"]
        # if the callback is a bot command, set it
        if "/" in message["data"] and "http" not in message["data"]:
            message_elements['bot_command'] = "bot_command"
        message_elements['user_id'] = message["from"]["id"]
        message_elements['chat_id'] = message["message"]["chat"]["id"]
        message_elements['is_bot'] = message["from"]["is_bot"]
        message_elements['chat_type'] = message["message"]["chat"]["type"]
        return message_elements
# ------ end: extract content of incoming messages

# ------ respond to incoming messages
    # create correct format for inline_keyboard 
    # e.g.: {"inline_keyboard":[[{"text": "Hello", "callback_url": "Hello", "url": "", "callback_data": "Hello"},{"text": "No", "callback_url": "Google", "url": "http://www.google.com/"}]]}
    def create_inline_keyboard(self, buttons):
        keyboard = []
        for item in buttons:
            # create format for button, e.g.: {"text": "Hello", "callback_url": "Hello", "url": "", "callback_data": "Hello"}
            button = {"text": item["title"], "callback_url": item["payload"], "url": "", "callback_data": item["payload"]}
            # append buttons to keyboard
            keyboard.append(button)
        # create required format for Telegram
        inline_keyboard = {"inline_keyboard": [keyboard]}

        return json.dumps(inline_keyboard)
# ------ end: respond to incoming messages

# ------ start: send messages
    def send_message(self, send_elements):
        parsed_message = urllib.parse.quote_plus(send_elements["message"])
        url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML&disable_web_page_preview=true".format(parsed_message, send_elements["chat_id"])
        # remove keyboard from the background if no new keyboard is provided
        if send_elements["keyboard"]:
            url += "&reply_markup={}".format(send_elements["keyboard"])
        else:
            url += "&reply_markup={\"remove_keyboard\":%20true}"
        # send message and save response
        url_response = Telegram_Bot.get_json_from_url(url)
        send_elements = Telegram_Bot.extract_message(send_elements, url_response["result"])
        Telegram_Bot.save_message(send_elements)
# ------ end: send messages