'''

Telegram_Sender sends messages to the user 

'''

import os
import json
import urllib
import requests

URL = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN')}/"

class Telegram_Sender:
    @staticmethod
    def get_chat_id_and_message_text_and_inline_keyboard(response):
        """
        Retrieve chat_id, message_text and inline_keyboard from response
            e.g. from {'recipient_id': 'test123', 'text': 'Hallo. Wie fühlst du dich?'} 
            to ('test_user', 'Hallo. Wie fühlst du dich?', None)
        """
        chat_id = response["recipient_id"]
        # if text provided, add respective message_element
        if response.get("text"):
            message_text = response["text"]
        else:
            message_text = None
        # if buttons provided, create inline keyboard
        if response.get('buttons'):
            inline_keyboard = Telegram_Sender._create_inline_keyboard(response["buttons"])
        else:
            inline_keyboard = None
        return chat_id, message_text, inline_keyboard

    @staticmethod
    def _create_inline_keyboard(buttons):
        """
        create correct format for inline_keyboard 
            e.g.: {"inline_keyboard":[[{"text": "Hello", "callback_url": "Hello", "url": "", "callback_data": "Hello"},
                    {"text": "No", "callback_url": "Google", "url": "http://www.google.com/"}]]}
        """
        keyboard = []
        for item in buttons:
            button = {"text": item["title"], "callback_url": item["payload"], "url": "", "callback_data": item["payload"]}
            keyboard.append(button)
        inline_keyboard = {"inline_keyboard": [keyboard]} # required format for Telegram
        return json.dumps(inline_keyboard)

    @staticmethod
    def send_message_to_telegram(chat_id, message_text, inline_keyboard):
        parsed_message = urllib.parse.quote_plus(message_text)
        url = URL + f"sendMessage?text={parsed_message}&chat_id={chat_id}&parse_mode=HTML&disable_web_page_preview=true"
        # remove keyboard from the background if no new keyboard is provided
        if inline_keyboard:
            url += f"&reply_markup={inline_keyboard}"
        else:
            url += "&reply_markup={\"remove_keyboard\":%20true}"
        requests.get(url) # post msg to Telegram server
