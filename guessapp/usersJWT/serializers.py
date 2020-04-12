from .models import User
from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username', 'email')

class UserRegiserSerializer(serializers.ModelSerializer):
		class Meta:
			model = User
			fields = ('id', 'username', 'verification_uuid', 'email')


class LoginSerializer(serializers.ModelSerializer):
	email = serializers.EmailField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(email=data['email'], password=data['password'])
		logger.warning(user)
		if user:
			if user.is_active and user.is_verified:
				return user
			else:
				raise serializers.ValidationError("User is not verified or active")
		else:
			raise serializers.ValidationError("Invalid Credentials")
	class Meta:
		model = User
		fields = ('id', 'email', 'password')
		extra_kwargs = {'password':{'write_only': True}}

class PasswordChangeSerializer(serializers.ModelSerializer):
	oldpassword = serializers.CharField()
	newpassword = serializers.CharField()

	def validate(self, data):
		user = User.objects.get(pk=self.initial_data['id'])
		if user.check_password(self.initial_data['oldpassword']):
			if user.is_active and user.is_verified:
				user.set_password(self.initial_data['newpassword'])
				user.save()
				return user
			else:
				raise serializers.ValidationError("User is not verified or active")
		else:
			raise serializers.ValidationError("Invalid Credentials")	

	class Meta:
		model = User
		fields = ('id', 'oldpassword', 'newpassword')
		extra_kwargs = {'newpassword':{'write_only': True},
		'oldpassword':{'write_only': True}}	

class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'password')
		extra_kwargs = {'password':{'write_only': True}}