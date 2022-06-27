from django.test import SimpleTestCase
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from django.urls import reverse, resolve
from api.views import get_all_create_new
from base.models import Passenger


class ApiUrlsTest(SimpleTestCase):
    def test_passenger_is_resolved(self):
        url = reverse('passenger')
        self.assertEquals(resolve(url).func, get_all_create_new)


class PassengerTest(APITestCase):
    passenger_url = reverse('passenger')

    def setUp(self):
        self.faker = Faker()
        Passenger.objects.create(firstName=self.faker.unique.first_name(),
                                 lastName=self.faker.unique.last_name(),
                                 email=self.faker.unique.email())

    def test_create(self):
        # data = {"firstName": self.faker.unique.first_name(),
        #         "lastName": self.faker.unique.last_name()}
        pass

    def test_get_all(self):
        response = self.client.get(self.passenger_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(list(response.json().keys()), [
                          "passengers", "result", "errorMessage"])
        self.assertTrue(len(response.json()["passengers"]) > 0)
        # self.assertTrue(response.json().keys())
