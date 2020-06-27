#!/usr/bin/python3.6
# coding: utf8

import os
import json
import requests

## call webhook to get appropriate response
def call_webhook(sender, message):
    msg_data = {"sender":sender,"message":message}

    response = requests.post(
        os.environ["RASA_WEBHOOK"], data=json.dumps(msg_data, ensure_ascii=False).encode('utf8'),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    return response.text