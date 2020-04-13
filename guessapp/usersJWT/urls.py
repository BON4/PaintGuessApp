from django.contrib import admin
from django.urls import path, include
from . import views
from knox import views as knox_views

urlpatterns = [
    #urls for Users
    path('', views.UsersListView.as_view(), name='users_list'),
    path('<int:pk>/', views.UsersDetailView.as_view(), name='users_detail'),
    path('verify/<uuid>/', views.user_verify, name='users-verify'), # registration verify
    #path('auth/', include('knox.urls')),
    path('register/', views.UsersRegisterView.as_view(), name='auth_users_register'),
    path('login/', views.UsersLoginView.as_view(), name='auth_users_login'),
    path('logout/', knox_views.LogoutAllView.as_view(), name='auth_users_logout'),
    path('change_password/', views.UserChangePasswordView.as_view(), name='auth_users_change_password'),
    path('reset_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

"""
POST ${API_URL}/reset_password/ - request a reset password token by using the email parameter
POST ${API_URL}/reset_password/confirm/ - using a valid token, the users password is set to the provided password
POST ${API_URL}/reset_password/validate_token/ - will return a 200 if a given token is valid
"""