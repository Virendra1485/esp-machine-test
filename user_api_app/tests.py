from django.test import TestCase
from .views import DeleteUserView, TokenGenerationAPIView
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.urls import reverse
from .views import UserUpdateAPIView, UserRegistrationAPIView


class DeleteUserViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(name="xyz", phone="7418529632", address="indore",
                                                         email="xyz@gmail.com", password="Test@123")
        access_token = AccessToken.for_user(self.user)
        self.token = str(access_token)

    def test_delete_user(self):
        url = reverse('delete-user')
        token_str = f"Bearer {self.token}"
        request = self.factory.delete(url, HTTP_AUTHORIZATION=token_str)
        view = DeleteUserView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(get_user_model().objects.filter(phone='7418529632').exists())
        self.assertEqual(response.data['message'], 'User deleted successfully')

    def test_unauthorized_user_deletion(self):
        url = reverse('delete-user')
        request = self.factory.delete(url)
        view = DeleteUserView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(get_user_model().objects.filter(phone='7418529632').exists())
        self.assertIn('detail', response.data)


class UserUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(phone='7418529632', name="xyz", email='xyz@gmail.com',
                                                         password='testpass', address="indore")
        access_token = AccessToken.for_user(self.user)
        self.token = str(access_token)

    def test_user_update(self):
        url = reverse('user-update')
        token_str = f"Bearer {self.token}"
        data = {'email': 'updated_email@gmail.com', 'address': 'bagli', 'name': 'abc'}

        request = self.factory.put(url, data, HTTP_AUTHORIZATION=token_str)
        view = UserUpdateAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, 'updated_email@gmail.com')
        self.assertEqual(updated_user.address, 'bagli')

    def test_unauthorized_user_update(self):
        url = reverse('user-update')
        data = {'email': 'updated_email@gmail.com', 'address': 'bagli', 'name': 'abc'}

        request = self.factory.put(url, data)
        view = UserUpdateAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenGenerationAPIViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(phone='7418529632', password='Test@123', name="abc",
                                                         address="indore", email="abc@gmail.com")

    def test_token_generation_success(self):
        url = reverse('user-sign-in')
        data = {'phone': '7418529632', 'password': 'Test@123'}
        request = self.factory.post(url, data)
        view = TokenGenerationAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('api_key', response.data)
        self.assertIn('secret_key', response.data)

    def test_token_generation_invalid_credentials(self):
        url = reverse('user-sign-in')
        data = {'phone': '7418529632', 'password': 'invalid_password'}
        request = self.factory.post(url, data)
        view = TokenGenerationAPIView.as_view()
        response = view(request)

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check if the response detail indicates invalid credentials
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials')


class UserRegistrationAPIViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.existing_user = get_user_model().objects.create_user(phone='1234567890', email='existing@gmail.com',
                                                                  password='Test@123', address="indore",
                                                                  name="existing")

    def test_user_registration(self):
        url = reverse('user-registration')
        data = {'phone': '7418529632', 'email': 'abc@gmail.com', 'password': 'Test@123', 'address': "inodre",
                "name": "abc"}
        request = self.factory.post(url, data)
        view = UserRegistrationAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(phone='7418529632').exists())

    def test_existing_username_registration(self):
        url = reverse('user-registration')
        data = {'phone': '1234567890', 'email': 'existing@gmail.com', 'password': 'Test@123', 'address': 'indore',
                'name': "existing"}
        request = self.factory.post(url, data)
        view = UserRegistrationAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('phone', response.data)
        self.assertIn('user with this phone already exists.', response.data['phone'])
