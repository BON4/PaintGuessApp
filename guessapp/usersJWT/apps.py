from django.apps import AppConfig


class UsersjwtConfig(AppConfig):
    name = 'usersJWT'

    def ready(self):
        import usersJWT.signals
