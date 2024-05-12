from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.generics import ListAPIView
from django.urls import reverse
from .views import BusinessRegistrationAPIView
from .serializers import BusinessSerializer
from .models import Business


class BusinessRegistrationAPIViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_business_registration_success(self):
        data = {'name': 'Test Business', 'email': 'test@example.com', 'address': '123 Test St.', "registration_number": "slkdfjkldjfkl", "phone": "7415144601"}
        request = self.factory.post(reverse('business-registration'), data, format='json')
        view = BusinessRegistrationAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertIn('api_key', response.data)
        self.assertIn('secret_key', response.data)

    def test_business_registration_invalid_data(self):
        data = {'name': '', 'email': 'invalid_email', 'address': '123 Test St.'}
        request = self.factory.post(reverse('business-registration'), data, format='json')
        view = BusinessRegistrationAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('email', response.data)


class BusinessListAPIViewTest(TestCase):
    def setUp(self):
        Business.objects.create(name='abc', email='abc@gamil.com', address='indore', phone="1478529632",
                                registration_number="54545481215")
        Business.objects.create(name='xyz', email='xyz@gmail.com', address='indore', phone="1479529632",
                                registration_number="5454548891215")

    def test_business_list(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('business-list'))

        view = ListAPIView.as_view(queryset=Business.objects.all(), serializer_class=BusinessSerializer)

        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'abc')
        self.assertEqual(response.data[1]['name'], 'xyz')
