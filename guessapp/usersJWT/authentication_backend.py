from django.contrib.auth.backends import ModelBackend
from .models import User


class UserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None):
        if email:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password) is True:
                    return user
            except User.DoesNotExist:
                pass
        elif username:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password) is True:
                    return user
            except User.DoesNotExist:
                pass