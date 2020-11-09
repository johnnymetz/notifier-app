from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send birthday notifier emails to a given set or all users."

    def add_arguments(self, parser):
        parser.add_argument(
            "emails", nargs="+", help="User emails. Use '*' for all users."
        )

    def handle(self, emails, *args, **kwargs):
        User = get_user_model()

        if "*" in emails:
            users = User.objects.filter(is_active=True, is_subscribed=True)
        else:
            users = []
            for email in emails:
                try:
                    user = User.objects.get(email=email)
                    if user.is_active and user.is_subscribed:
                        if user not in users:
                            users.append(user)
                    else:
                        self.stdout.write(
                            self.style.ERROR(f"{email} is inactive or unsubscribed.")
                        )
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"{email} does not exist."))

        for user in users:
            user.send_birthday_notifier_email()
            self.stdout.write(self.style.SUCCESS(f"{user} successfully notified."))
