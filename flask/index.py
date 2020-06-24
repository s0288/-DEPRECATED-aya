# / index.py
from flask import Flask, request, jsonify, render_template
import requests
import json

import telegram

Telegram_Bot = telegram.Telegram_Bot()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bot', methods=['POST'])
def webhook():    
    response = request.get_json(silent=True)
    send_elements = get_send_elements(response)
    # send outgoing message
    Telegram_Bot.send_message(send_elements)

    return response


def get_send_elements(response):
    ## -----------
    ## receive msg, e.g. {'recipient_id': 'test123', 'text': 'Hallo. Wie fühlst du dich?'} and send/save response
    ## -----------
    # message container for incoming and outgoing msgs
    send_elements = {'created_at': None, 'received_at': None, 'message_id': None,
                    'message': None, 'user_id': None, 'chat_id': None, 'chat_type': None, 'is_bot': None, 
                    'bot_command': None, 'keyboard': None, 'img': None}
    send_elements["chat_id"] = response["recipient_id"]
    # if text provided, add respective message_element
    if response.get("text"):
        send_elements["message"] = response["text"]
    # if image provided, add respective message_element
    if response.get("image"):
        send_elements["message"] = response["image"]
    # if buttons provided, create inline keyboard
    if response.get('buttons'):
        # create correct format for inline_keyboard, e.g.: {"inline_keyboard":[[{"text": "Hello", "callback_url": "Hello", "url": "", "callback_data": "Hello"},{"text": "No", "callback_url": "Google", "url": "http://www.google.com/"}]]}
        send_elements["keyboard"] = Telegram_Bot.create_inline_keyboard(response["buttons"])
    return send_elements




# run Flask app
if __name__ == "__main__":
    app.run()