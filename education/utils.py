from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
import requests

sched = BlockingScheduler()


def send_test_results_to_parent(text):
    apiToken = settings.BOT_TOKEN

    apiURL = f"https://api.telegram.org/bot{apiToken}/sendMessage"

    try:
        response = requests.post(
            apiURL, json={"chat_id": "403730093", "text": "qannne"}
        )
        print(response.text)
    except Exception as e:
        print(e)
