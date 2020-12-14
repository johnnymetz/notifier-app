# import logging
#
# from django.contrib.auth.models import User
#
# from celery import shared_task
#
# from notifier.user_helpers import send_events_email_to_user
#
# logger = logging.getLogger("django")
#
#
# @shared_task
# def send_events_email_to_user_task(username):
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         raise Exception(f"User {username} does not exist.")
#     sent = send_events_email_to_user(user=user)
#     if sent:
#         logger.debug(f"Email to {user} successfully sent.")
#     return sent
