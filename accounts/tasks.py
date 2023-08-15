from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from environs import Env
from django_project.settings import EMAIL_HOST_USER
from django_project import celery_app


env = Env()
env.read_env()


# Test purpose
@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# In work
@shared_task()
def send_feedback_email_after_account_creation_task(message):
    """Sends an email when user creates an account."""
    sleep(10)  # Simulate operation time that Django needs synchronously
    send_mail(
        "Hi,",
        f"\t{message}\n\nThank you for choosing best restaurant app in the world... no in the galaxy!",
        EMAIL_HOST_USER,
        ['misk0005@wp.pl'],
        fail_silently=False,
    )
