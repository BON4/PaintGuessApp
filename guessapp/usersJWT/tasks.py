from celery import shared_task, task
from django.core.mail import send_mail, send_mass_mail, BadHeaderError
import logging
import random
from smtplib import SMTPException
import logging
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(SMTPException,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def confirm_email(self, data):
    logger.info("DDDDDDDDd")
    logger.info(data)
    try:
        send_mail(
            subject='Subject',
            message='Follow this link to verify your account: http://127.0.0.1:8000%s'
            % reverse('users-verify', kwargs={'uuid': str(data['verification_uuid'])}),
            from_email='silvia.homam@gmail.com',
            recipient_list=[data['email']],
            fail_silently=False,
        )
    except BadHeaderError:
        print("Program found a newline character. This is injection defender exception !")


@shared_task(bind=True, autoretry_for=(SMTPException,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def reset_password_task(self, sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    }

    # render email text
    #email_html_message = render_to_string('email/user_reset_password.html', context)
    #email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        "{}?token={}".format(
            reverse('password_reset:reset-password-request'), reset_password_token.key),
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    #msg.attach_alternative(email_html_message, "text/html")
    msg.send()

# pylint: skip-file
