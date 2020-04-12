from django.conf import settings
from django.shortcuts import render
from .models import User
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.models import AuthToken
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.signals import user_logged_out
from .serializers import (
						UserSerializer,
						RegisterSerializer,
						LoginSerializer,
						UserRegiserSerializer,
						PasswordChangeSerializer
						)
import logging

logger = logging.getLogger(__name__)

class UsersDetailView(generics.RetrieveUpdateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = 'pk'

class UsersRegisterView(generics.GenericAPIView):
	permission_classes = (AllowAny,)
	serializer_class = RegisterSerializer

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return Response({
			"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(user)[1]
		})

class UsersLoginView(generics.GenericAPIView):
	permission_classes = (AllowAny,)
	serializer_class = LoginSerializer

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		return Response({
			"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(user)[1]
		})

class UserChangePasswordView(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = PasswordChangeSerializer

	def post(self, request):
		#logger.info(request.user)
		serializer = self.get_serializer(data={'id':request.user.id,
		 'newpassword':request.POST['newpassword'],
		 'oldpassword':request.POST['oldpassword']})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		return Response({
			"user": UserSerializer(user, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(user)[1]
		})	


@api_view(['GET'])
def user_verify(request, uuid):
		try:
			user = User.objects.get(verification_uuid=uuid, is_verified=False)
		except User.DoesNotExist:
			return Response(
				status=status.HTTP_404_NOT_FOUND
			)

		user.is_verified = True
		user.save()
		return Response(
			status=status.HTTP_202_ACCEPTED
		)	

        
class UsersListView(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = User.objects.all()
	serializer_class = UserSerializer