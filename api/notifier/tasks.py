from celery import shared_task
from celery.utils.log import get_task_logger
from notifier.helpers import send_birthday_notifier_email
from notifier.models import Friend

logger = get_task_logger(__name__)


@shared_task
def send_birthday_notifier_email_task(to):
    # TODO: get today's bdays only
    friends = Friend.objects.all()[5:10]
    logger.info("Sending email...")
    sent = send_birthday_notifier_email(friends=friends, to=to)
    return sent
