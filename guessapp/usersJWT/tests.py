from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from knox.models import AuthToken
from .models import User
import json
class UserTokenTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='vlad', email='silvia.homam@gmail.com', password='1488')
        self.user.is_verified = True
        self.user.save()


    def test_login_verifyed(self):
        c = APIClient()
        user_dict = {
            "email": self.user.email,
            "password": "1488"
        }
        response  = c.post('http://127.0.0.1:8000/users/login/', json.dumps(user_dict),content_type="application/json")
        token = response.data['token']
        self.assertTrue(status.is_success(response.status_code)) #Check if user has been logged in 
        self.assertTrue(token) #Check if token has been created 

    def test_logout_verifyed(self):
        #Specifing header with auth token
        c = APIClient()
        user_dict = {
            "email": self.user.email,
            "password": "1488"
        }
        response  = c.post('http://127.0.0.1:8000/users/login/', json.dumps(user_dict),content_type="application/json")
        
        token = response.data['token']

        response = c.get('http://127.0.0.1:8000/users/logout/', HTTP_AUTHORIZATION='Token {}'.format(token))
        print(response)

        self.assertFalse(AuthToken.objects.filter(digest=token))
