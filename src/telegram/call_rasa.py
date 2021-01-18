#!/usr/bin/python3.6
# coding: utf8

import os
import json
import requests

def call_rasa(sender, message):
    """
    call Rasa to get appropriate response.
    Rasa's callback channel is defined as "http://<host>:<port>/webhooks/callback/webhook" 
        (see here: https://rasa.com/docs/rasa/connectors/your-own-website)
    It is necessary to use Rasa's callback channel because the REST channel does not allow to add custom triggers
    """
    msg_data = {"sender":sender,"message":message}

    response = requests.post(
        os.environ.get("RASA_WEBHOOK"), data=json.dumps(msg_data, ensure_ascii=False).encode('utf8'),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    return response.text