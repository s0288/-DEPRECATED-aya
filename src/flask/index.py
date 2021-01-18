# / index.py

from flask import Flask, request, jsonify, render_template
import logging

from telegram_sender import Telegram_Sender
Telegram_Sender = Telegram_Sender()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bot', methods=['POST'])
def webhook():
    response = request.get_json()
    # app.logger.info(f"response received: {response}")
    chat_id, message_text, inline_keyboard = Telegram_Sender.get_chat_id_and_message_text_and_inline_keyboard(response)
    Telegram_Sender.send_message_to_telegram(chat_id, message_text, inline_keyboard)
    return response

# run Flask app
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
    app.run()