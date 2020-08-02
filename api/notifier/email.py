from typing import Optional

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from notifier.exceptions import NotifierException
from notifier.user_helpers import get_birthday_email_context


def send_notifier_email(
    subject: str,
    text_content: str,
    html_content: str,
    to: str,
    from_email: Optional[str] = None,
):
    """
    from_email defaults to DEFAULT_FROM_EMAIL,
    except when using gmail which defaults to EMAIL_HOST_USER
    """
    msg = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=[to]
    )
    msg.attach_alternative(html_content, "text/html")
    sent = msg.send()
    return sent


def send_birthday_notifier_email_to_user(user: User, from_email: Optional[str] = None):
    if not user.email:
        raise NotifierException(f"{user} must provide an email.")
    context = get_birthday_email_context(user)
    text_content = render_to_string("notifier/birthdays-email.txt", context)
    html_content = render_to_string("notifier/birthdays-email.html", context)
    sent = send_notifier_email(
        subject="Today's Birthdays",
        text_content=text_content,
        html_content=html_content,
        to=user.email,
        from_email=from_email,
    )
    return sent
