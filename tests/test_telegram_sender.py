'''

tests for Telegram_Listener

'''
import pytest

from flask.telegram_sender import Telegram_Sender
Telegram_Sender = Telegram_Sender()

@pytest.mark.parametrize("response, expected", [
    (
        {'recipient_id': 'test_user', 'text': 'Hallo. Wie fühlst du dich?'}
        , ('test_user', 'Hallo. Wie fühlst du dich?', None)
    ), (
        {'recipient_id': 'test_user', 'text': 'Du fastest seit 12 Stunden und 31 Minuten. Möchtest du das Fasten jetzt beenden?', 
            'buttons': [{'payload': 'ja', 'title': 'ja'}, {'payload': 'nein', 'title': 'nein'}]}
        , (
            'test_user', 
            'Du fastest seit 12 Stunden und 31 Minuten. Möchtest du das Fasten jetzt beenden?', 
            '{"inline_keyboard": [[{"text": "ja", "callback_url": "ja", "url": "", "callback_data": "ja"}, ' \
                '{"text": "nein", "callback_url": "nein", "url": "", "callback_data": "nein"}]]}')
    )
    ], ids=["plain", "with_inline_keyboard"]
)
def test_telegram_sender_get_chat_id_and_message_text_and_inline_keyboard(response, expected):
    assert Telegram_Sender.get_chat_id_and_message_text_and_inline_keyboard(response) == expected
