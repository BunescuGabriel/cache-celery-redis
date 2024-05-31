from Magazin.celery import app
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings

@app.task
def send_spam_email(email):
    send_mail(
        'Hello from Celery',
        'This is a test message from Celery',
        'settings.EMAIL_HOST_USER',
        [email],
        fail_silently=False,
    )


@app.task
def send_best_email():
    for contact in Contact.objects.all():
        send_mail(
            'Hello from Celery',
            'Hello motherfucker ne vedem peste o minuta',
            'settings.EMAIL_HOST_USER',
            [contact.email],
            fail_silently=False,
        )

