from typing import List, Optional

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_notifier_email(
    subject: str,
    text_content: str,
    html_content: str,
    to: str,
    from_email: Optional[str] = None,
):
    """
    from_email defaults to EMAIL_HOST_USER when using Gmail
    """
    # text_content = "This is an important message."
    # html_content = "<p>This is an <strong>important</strong> message.</p>"
    msg = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=[to]
    )
    msg.attach_alternative(html_content, "text/html")
    sent = msg.send()
    return sent


def send_birthday_notifier_email(
    friends: List[User], to: str, from_email: Optional[str] = None
):
    context = {"friends": friends}
    text_content = render_to_string("notifier/birthdays-email.txt", context)
    html_content = render_to_string("notifier/birthdays-email.html", context)
    sent = send_notifier_email(
        subject="Today's Birthdays",
        text_content=text_content,
        html_content=html_content,
        to=to,
        from_email=from_email,
    )
    return sent
