"""

telgram_listener listens for incoming messages or requests to send triggers 

"""

import os
import requests
import json

URL = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN')}/"

class Telegram_Listener:
    def get_update_and_next_update_id(self, offset=None):
        """
            Retrieve incoming msgs.

            Telegram saves all incoming msgs into an update json that looks like this:
                {"ok":True,"result":[
                    {"update_id":161176028,"message":{"message_id":811,
                        "from":{"id":TELEGRAM_USER_ID,"is_bot":False,"first_name":"TELEGRAM_FIRST_NAME","language_code":"en"},
                        "chat":{"id":TELEGRAM_USER_ID,"first_name":"TELEGRAM_FIRST_NAME","type":"private"},
                        "date":1610819511,"text":"Hi there"}},
                    {"update_id":161176029, ...}
                ]}
            
            It is possible that Telegram does not update the result json before polling occurs again. 
            To prevent retrieving the same msg twice, ignore the already retrieved update_ids with next_update_id.

            :param offset:                  int     (ignore all update_ids until the requested offset)
            :return:        js              json    (json that contains incoming msgs)
                            next_update_id  int     (min(update_id)+1 in json)
        """
        url = URL + "getUpdates?timeout=600"
        if offset:
            url += "&offset={}".format(offset)
        
        js = Telegram_Listener._get_updates_from_telegram_or_answer_callback(url)
        update, next_update_id = Telegram_Listener._get_update_and_next_update_id(js)
        
        return update, next_update_id

    @staticmethod
    def _get_updates_from_telegram_or_answer_callback(url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        js = json.loads(content)
        return js

    @staticmethod
    def _get_update_and_next_update_id(js):
        """
        Telegram_Listener processes one message per call. 
        Therefore, it is not necessary to load all available updates, since only the oldest update will be processed in the call.
        """
        if any(js["result"]):
            update_id = min([row["update_id"] for row in js["result"]])
            update = [row for row in js["result"] if row["update_id"] == update_id][0]
            return update, update_id+1
        else: 
            return None, None

    def extract_main(self, update):
        extraction_method = Telegram_Listener._set_extraction_method(update) 
        if extraction_method == 'do_not_extract':
            return None, None
        if extraction_method == 'extract_message':
            chat_id, message_text = Telegram_Listener._extract_message(update['message'])
        elif extraction_method == 'extract_callback':
            Telegram_Listener._answer_callback(update['callback_query']['id'])
            chat_id, message_text = Telegram_Listener._extract_callback(update['callback_query'])
        return chat_id, message_text

    @staticmethod
    def _set_extraction_method(update):
        """
        these extraction methods exist: [message, callback, not-to-be-extracted content]
        """
        if update.get('message'):
            if any(update["message"].get(key) for key in ['group_chat_created', 'new_chat_participant', 'left_chat_participant']): 
                # ignore out-of-the-ordinary actions
                logging.info("received a do_not_extract_event")
                return 'do_not_extract'
            return 'extract_message'
        elif update.get('callback_query') is not None:
            return 'extract_callback'
        else:
            return 'do_not_extract'

    @staticmethod
    def _extract_message(update_message):
        chat_id = update_message["chat"]["id"]
        
        if update_message.get('text'):
            message_text = update_message["text"]
        elif update_message.get('document'): # e.g. pdf
            message_text = 'file: ' + update_message["document"]["file_id"]
        elif update_message.get('photo'): # e.g. jpg
            try:
                message_text = 'file: ' + update_message["photo"][3]["file_id"]
            except:
                message_text = 'file: ' + update_message["photo"][0]["file_id"]
        
        return chat_id, message_text

    @staticmethod
    def _extract_callback(update_message):
        chat_id = update_message["message"]["chat"]["id"]
        message_text = update_message["data"]
        return chat_id, message_text

    @staticmethod
    def _answer_callback(callback_query_id):
        """
        answering a callback is necessary to unfreeze the user's telegram chat (e.g. for inline buttons)
        """
        url = URL + f"answerCallbackQuery?callback_query_id={callback_query_id}"
        Telegram_Listener._get_updates_from_telegram_or_answer_callback(url)
