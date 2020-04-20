from celery import shared_task
from notifier.helpers import send_birthday_notifier_email_to_all_users


@shared_task
def send_birthday_notifier_email_to_all_users_task():
    return send_birthday_notifier_email_to_all_users
