from django.test import SimpleTestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from faker import Faker
from django.urls import reverse, resolve
from api.views.passengerView import PassengerView
from api.views.passengerDetailView import PassengerDetailView
from base.models import Passenger
from .standards import ResultTypes


class PassengerTestBase:
    passengerUrl = reverse('passenger')
    resolvedPassengerUrl = resolve(passengerUrl)
    passengerDetailUrl = reverse('passengerDetail', args=[1])
    resolvedPassengerDetailUrl = resolve(passengerDetailUrl)


class Utility:
    def compareObjects(data: dict, response: dict):
        dataKeys = list(data.keys())
        dataKeys.append("id")

        if sorted(dataKeys) != sorted(list(response.keys())):
            return False

        for key in data.keys():
            if data[key] != response[key]:
                return False

        return True


class ApiUrlsTest(SimpleTestCase, PassengerTestBase):
    def test_passengerIsResolved(self):
        self.assertEquals(self.resolvedPassengerUrl.func.view_class,
                          PassengerView)

    def test_passengerDetailIsResolved(self):
        self.assertEquals(self.resolvedPassengerDetailUrl.func.view_class,
                          PassengerDetailView)


class PassengerTest(APITestCase, PassengerTestBase):

    def setUp(self):
        self.client = APIClient()
        self.faker = Faker()
        for _ in range(3):
            Passenger.objects.create(firstName=self.faker.unique.first_name(),
                                     lastName=self.faker.unique.last_name(),
                                     email=self.faker.unique.email())

    def test_getAll(self):
        response = self.client.get(self.passengerUrl)

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,
                          "Status Code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["passengers", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertTrue(len(response.json()["passengers"]) > 0,
                        "Returned no passengers")
        self.assertEquals(response.json()["result"],
                          ResultTypes.RETRIEVED,
                          "Returned result value is not correct")

    def test_create(self):
        data = {"firstName": self.faker.unique.first_name(),
                "lastName": self.faker.unique.last_name(),
                "email": self.faker.unique.email()}
        response = self.client.post(self.passengerUrl, data=data)

        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED,
                          "Status Code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["passengers", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertEquals(response.json()["result"],
                          ResultTypes.CREATED,
                          "Returned result value is not correct.")


class PassengerDetailTest(APITestCase, PassengerTestBase):

    def setUp(self):
        self.client = APIClient()
        self.faker = Faker()
        for _ in range(1):
            Passenger.objects.create(firstName=self.faker.unique.first_name(),
                                     lastName=self.faker.unique.last_name(),
                                     email=self.faker.unique.email())

    def test_get_one(self):
        response = self.client.get(self.passengerDetailUrl)
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,
                          "Status Code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["passengers", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertTrue('id' in response.json()["passengers"].keys(),
                        "Returned passenger object has no id key")
        self.assertEquals(response.json()["result"],
                          ResultTypes.RETRIEVED,
                          "Returned result value is not correct")

    def test_update(self):
        data = {"firstName": self.faker.unique.first_name(),
                "lastName": self.faker.unique.last_name(),
                "email": self.faker.unique.email()}

        response = self.client.put(self.passengerDetailUrl, data=data)

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK, "Status code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["passengers", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertTrue('id' in response.json()["passengers"].keys(),
                        "Returned passenger object has no id key")
        self.assertTrue(Utility.compareObjects(data, response.json()[
                        "passengers"]), "Updated data is not correct")

    def test_delete(self):

        responseDel = self.client.delete(self.passengerDetailUrl)
        responseGet = self.client.get(self.passengerDetailUrl)

        self.assertEquals(responseDel.status_code,
                          status.HTTP_204_NO_CONTENT,
                          "Status code is not correct")
        self.assertEquals(responseDel.data["result"],
                          ResultTypes.DELETED,
                          "Returned result is not correct")
        self.assertAlmostEquals(responseGet.status_code,
                                status.HTTP_404_NOT_FOUND,
                                "Data is not deleted.")
