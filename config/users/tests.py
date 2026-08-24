from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@test.com',
            username='user',
            password='User12345'
        )

    def test_register_user(self):
        user = User.objects.create_user(
            email='new@test.com',
            username='newuser',
            password='NewUser12345'
        )
        self.assertTrue(User.objects.filter(email='new@test.com').exists())
        self.assertEqual(user.email, 'new@test.com')

    def test_login_user(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'user@test.com',
            'password': 'User12345'
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_get_token(self):
        response = self.client.post(reverse('users:api_token'), {
            'username': 'user@test.com',
            'password': 'User12345'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_list_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('users:api_users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
