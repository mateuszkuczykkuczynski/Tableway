from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from environs import Env

from django_project import celery_app


env = Env()
env.read_env()


# Test purpose
@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# In work
@shared_task()
def send_feedback_email_table_booking_task(email_address, message, restaurant_name):
    """Sends an email when the feedback form has been submitted."""
    sleep(10)  # Simulate operation time that Django needs synchronously
    send_mail(
        "Hi",
        f"\t{message}\n\nYou have booked a table in {restaurant_name}, we hope you enjoyed using Tableway! "
        f"Thanks for choosing us!",
        env("EMAIL_ADDRESS"),
        [email_address],
        fail_silently=False,
    )
