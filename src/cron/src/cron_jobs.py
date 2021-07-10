'''

To make sure that bugs or errors are caught early, an alerting system is required to inform about system activity. 
Uptime_Bot triggers msgs to the Flask app to trigger Telegram msgs to the root user. 

'''

import os
import logging
import crython

from utils import postgres_engine
# from is_active import is_active
from fasting_report import fasting_report

ROOT_USER = os.environ.get("ROOT_USER")
FLASK_URL = os.environ.get("FLASK_URL")
ENGINE = postgres_engine()

# @crython.job(expr='@daily', root_user=ROOT_USER, flask_url=FLASK_URL, engine=ENGINE)
# def cron_is_active(root_user, flask_url, engine):
#     """ cronjob wrapper for is_active """
#     is_active(root_user, flask_url, engine)

@crython.job(expr='@daily', flask_url=FLASK_URL, engine=ENGINE)
def cron_fasting_report(flask_url, engine, last_n_days=7):
    """ cronjob wrapper for fasting report """
    fasting_report(flask_url, engine, last_n_days)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
    crython.start()
    crython.join()  ## This will block
