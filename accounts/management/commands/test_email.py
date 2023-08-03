from django.core.management.base import BaseCommand

from accounts.tasks import send_feedback_email_task


class Command(BaseCommand):
    help = 'Sends a test email'

    def handle(self, *args, **kwargs):
        email_address = 'test@example.com'  # replace with your email
        message = 'This is a test message'
        send_feedback_email_task.delay(message)
        self.stdout.write(self.style.SUCCESS('Successfully sent test email'))
