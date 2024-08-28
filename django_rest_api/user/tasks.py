from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_confirmation_email(recipient_list):
    subject = 'Confirm your Email Address'
    message = 'Thank you for registering. Please confirm your email by clicking the following link.'
    email = EmailMessage(subject, message, to=recipient_list)
    email.send()
