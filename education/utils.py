from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import requests

from .models import (
    OrderTestInfo,
    OrderTestInfoAssignStudent,
    OrderTestPack,
    OrderTestPackResultsOfStudent,
)

sched = BackgroundScheduler()


def send_test_results_to_parent(order_test_info_id):
    apiToken = settings.BOT_TOKEN
    message = ""
    apiURL = f"https://api.telegram.org/bot{apiToken}/sendMessage"

    order_test_assigned_student = OrderTestInfoAssignStudent.objects.filter(
        order_test_info_id=order_test_info_id
    )

    for x in order_test_assigned_student:
        if x.submitted == True:
            count = 0
            order_test_pack = OrderTestPack.objects.filter(
                order_test_info_id=order_test_info_id
            )
            test_submitted_students = OrderTestPackResultsOfStudent.objects.filter(
                student=x.student
            )
            for x in test_submitted_students:
                if x.is_correct == True:
                    count = count + 1

    try:
        response = requests.post(
            apiURL, json={"chat_id": "403730093", "text": "qannne"}
        )
        print(response.text)
    except Exception as e:
        print(e)
