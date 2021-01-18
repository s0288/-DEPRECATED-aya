'''

To make sure that bugs or errors are caught early, an alerting system is required to inform about system activity. 
Uptime_Bot triggers msgs to the Flask app to trigger Telegram msgs to the root user. 

'''

import crython
import requests
import os

@crython.job(expr='@daily', root_user=os.environ.get("ROOT_USER"), flask_url=os.environ.get("FLASK_URL"))
def is_active(root_user, flask_url):
    '''
    When Uptime_Bot is initialised, trigger a msg.
    '''
    url = flask_url
    data = {"recipient_id":root_user,"text":"Uptime Bot ist aktiv"}
    requests.post(url, json=data)


if __name__ == "__main__":
    crython.start()
    crython.join()  ## This will block    
