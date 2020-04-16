from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .tasks import confirm_email, reset_password_task
from .serializers import UserRegiserSerializer
from django_rest_passwordreset.signals import reset_password_token_created
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_has_been_created(sender, instance, created, **kwargs):
    if created:
        data = UserRegiserSerializer(instance).data
        confirm_email.delay(data)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    reset_password_task(
        sender, instance, reset_password_token, *args, **kwargs)
# pylint: skip-file
