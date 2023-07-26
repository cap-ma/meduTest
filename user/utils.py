import requests
from django.conf import settings
import datetime
from datetime import date


def send_to_telegram(chat_id, first_name, last_name, status):
    messsage = f"{first_name} {last_name} {datetime.date} darsga {status}"
    apiToken = settings.BOT_TOKEN

    apiURL = f"https://api.telegram.org/bot{apiToken}/sendMessage"

    try:
        response = requests.post(apiURL, json={"chat_id": chat_id, "text": messsage})
        print(response.text)
    except Exception as e:
        print(e)
