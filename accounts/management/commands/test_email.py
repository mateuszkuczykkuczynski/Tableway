from django.core.management.base import BaseCommand

from accounts.tasks import send_feedback_email_task


class Command(BaseCommand):
    help = 'Sends a test email'

    def handle(self, *args, **kwargs):
        email_address = 'misk0005@wp.pl'  # replace with your email
        message = 'This is a test message from Tableway'
        send_feedback_email_task.delay(email_address, message)
        self.stdout.write(self.style.SUCCESS('Successfully sent test email'))
