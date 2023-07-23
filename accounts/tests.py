from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('create_user')

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
