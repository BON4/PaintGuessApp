from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.conf import settings
import django.dispatch

django.dispatch.Signal()

import logging
logger = logging.getLogger(__name__)

class UserAccountManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **kwargs):

		if not username:
			raise ValueError("Username must be provided")

		if not email:
			raise ValueError("Email must be provided")

		if not password:
			raise ValueError("Password must be provided")
		
		
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **kwargs)
		user.set_password(password)
		user.save(using= self._db)
		return user

	def create_user(self, username=None, email=None, password=None, **kwargs):
		return self._create_user(username, email, password, **kwargs)

	def create_superuser(self, username, email, password, **kwargs):
		kwargs['is_staff'] = True
		kwargs['is_superuser'] = True
		return self._create_user(username, email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
	REQUIRED_FIELDS = ['email']
	USERNAME_FIELD = 'username'
	EMAIL_FIELD = 'email'

	objects = UserAccountManager()

	username = models.CharField('username', max_length=200, unique=True)
	email = models.EmailField('email', unique=True, blank=False, null=False)
	is_staff = models.BooleanField('staff status', default=False)
	is_active = models.BooleanField('active status', default=True)
	is_verified = models.BooleanField('verified', default=False)
	verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

	def save(self, *args, **kwargs):
		super(User, self).save(*args, **kwargs)

	def get_class(self):
		return self.__class__

	def __str__(self):
		return str(self.username)

	def get_email(self):
		return self.email

	def __unicode__(self):
		return self.email
