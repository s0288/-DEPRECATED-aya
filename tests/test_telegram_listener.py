'''

tests for Telegram_Listener

'''
import pytest

import telegram.telegram_listener
Telegram_Listener = telegram.Telegram_Listener()

@pytest.mark.parametrize("json, expected", [
    (
        {"ok":True,"result":[
            {"update_id":161176028,"message":{"message_id":811,"from":{"id":"TELEGRAM_USER_ID","is_bot":False,
                "first_name":"TELEGRAM_FIRST_NAME","language_code":"en"},
                "chat":{"id":"TELEGRAM_USER_ID","first_name":"TELEGRAM_FIRST_NAME","type":"private"},"date":1610819511,"text":"hi there"}},
            {"update_id":161176029,"message":{"message_id":812,"from":{"id":"TELEGRAM_USER_ID","is_bot":False,
                "first_name":"TELEGRAM_FIRST_NAME","language_code":"en"},
                "chat":{"id":"TELEGRAM_USER_ID","first_name":"TELEGRAM_FIRST_NAME","type":"private"},"date":1610819511,"text":"how are you?"}}]}
        , ({"update_id":161176028,"message":{"message_id":811,"from":{"id":"TELEGRAM_USER_ID","is_bot":False,
                "first_name":"TELEGRAM_FIRST_NAME","language_code":"en"},
                "chat":{"id":"TELEGRAM_USER_ID","first_name":"TELEGRAM_FIRST_NAME","type":"private"},"date":1610819511,"text":"hi there"}}
            , 161176029)
    ),
    (
        {"ok":True,"result":[]}, (None, None)
    )
    ],
        ids=[
            "with_updates", 
            "without_updates"
            ]
)
def test_telegram_listener__get_update_and_next_update_id(json, expected):
    assert Telegram_Listener._get_update_and_next_update_id(json) == expected


@pytest.mark.parametrize("update_message, expected", [
    (
        {'message_id': 813, 'from': {'id': 'TELEGRAM_USER_ID', 'is_bot': False, 'first_name': 'TELEGRAM_FIRST_NAME', 'language_code': 'en'}, 
            'chat': {'id': 'TELEGRAM_USER_ID', 'first_name': 'TELEGRAM_FIRST_NAME', 'type': 'private'}, 'date': 1610819512, 'text': 'hej'}
        , ('TELEGRAM_USER_ID', 'hej')
    ), (
        {'message_id': 850, 'from': {'id': 'TELEGRAM_USER_ID', 'is_bot': False, 'first_name': 'TELEGRAM_FIRST_NAME', 'language_code': 'fr'}, 
            'chat': {'id': 'TELEGRAM_USER_ID', 'first_name': 'TELEGRAM_FIRST_NAME', 'type': 'private'}, 'date': 1610880052, 
            'photo': [{'file_id': 'FILE_ID_0', 
            'file_unique_id': 'FILE_UNIQUE_ID', 'file_size': 27703, 'width': 320, 'height': 180}, 
            {'file_id': 'FILE_ID_1', 
                'file_unique_id': 'FILE_UNIQUE_ID', 'file_size': 160300, 'width': 800, 'height': 450}, 
            {'file_id': 'FILE_ID_2', 
                'file_unique_id': 'FILE_UNIQUE_ID', 'file_size': 346540, 'width': 1280, 'height': 720}]}
        , ('TELEGRAM_USER_ID', 'file: FILE_ID_0')
    ), (
        {'message_id': 856, 'from': {'id': 'TELEGRAM_USER_ID', 'is_bot': False, 'first_name': 'TELEGRAM_FIRST_NAME', 'language_code': 'fr'}, 
            'chat': {'id': 'TELEGRAM_USER_ID', 'first_name': 'TELEGRAM_FIRST_NAME', 'type': 'private'}, 'date': 1610882310, 
            'document': {'file_name': 'fastenkur_programm.rtf', 'mime_type': 'text/rtf', 'file_id': 'FILE_ID_0', 
                'file_unique_id': 'FILE_UNIQUE_ID', 'file_size': 857}}
        , ('TELEGRAM_USER_ID', 'file: FILE_ID_0')
    ), (
        {'message_id': 857, 'from': {'id': 'TELEGRAM_USER_ID', 'is_bot': False, 'first_name': 'TELEGRAM_FIRST_NAME', 'language_code': 'fr'}, 
            'chat': {'id': 'TELEGRAM_USER_ID', 'first_name': 'TELEGRAM_FIRST_NAME', 'type': 'private'}, 'date': 1610882371, 
            'document': {'file_name': 'sample.pdf', 'mime_type': 'application/pdf', 
                'thumb': {'file_id': 'FILE_ID_0', 'file_unique_id': 'FILE_UNIQUE_ID', 'file_size': 5442, 'width': 247, 'height': 320}, 
                    'file_id': 'FILE_ID_0', 'file_unique_id': 'FILE_UNIQUE_ID', 'file_size': 3028}}
        , ('TELEGRAM_USER_ID', 'file: FILE_ID_0')
    )
    ], ids=["regular", "img upload", "doc upload 1", "doc upload 2"]
)
def test_telegram_listener__extract_message(update_message, expected):
    assert Telegram_Listener._extract_message(update_message) == expected


@pytest.mark.parametrize("update_message, expected", [
    (
        {'id': '1785005942255623485', 'from': {'id': 'TELEGRAM_USER_ID', 'is_bot': False, 'first_name': 'TELEGRAM_FIRST_NAME', 'language_code': 'en'}, 
            'message': {'message_id': 805, 'from': {'id': 1341457071, 'is_bot': True, 'first_name': 'aya_test_local', 'username': 'aya_test_local_bot'}, 
            'chat': {'id': 'TELEGRAM_USER_ID', 'first_name': 'TELEGRAM_FIRST_NAME', 'type': 'private'}, 'date': 1610801142, 
            'text': 'Du fastest seit 12 Stunden und 17 Minuten. Möchtest du das Fasten jetzt beenden?', 
            'reply_markup': {'inline_keyboard': [[{'text': 'ja', 'callback_data': 'ja'}, 
            {'text': 'nein', 'callback_data': 'nein'}]]}}, 'chat_instance': '630986056078679937', 'data': 'ja'}
        , ('TELEGRAM_USER_ID', 'ja')
    )
    ], ids=["regular"]
)
def test_telegram_listener__extract_callback(update_message, expected):
    assert Telegram_Listener._extract_callback(update_message) == expected
