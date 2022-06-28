import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.test import SimpleTestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from faker import Faker
from django.urls import reverse, resolve
from api.views.passengerView import PassengerView
from api.views.passengerDetailView import PassengerDetailView
from api.views.tripDetailView import TripDetailView
from api.views.tripView import TripView
from base.models import Passenger, Trip
from .standards import ResultTypes


class PassengerTestBase:
    passengerUrl = reverse('passenger')
    resolvedPassengerUrl = resolve(passengerUrl)
    passengerDetailUrl = reverse('passengerDetail', args=[1])
    resolvedPassengerDetailUrl = resolve(passengerDetailUrl)


class TripTestBase:
    tripUrl = reverse('trip')
    resolvedTripUrl = resolve(tripUrl)
    tripDetailUrl = reverse('tripDetail', args=[1])
    resolvedTripDetailUrl = resolve(tripDetailUrl)


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


class ApiUrlsTest(SimpleTestCase, PassengerTestBase, TripTestBase):
    def test_passengerIsResolved(self):
        self.assertEquals(self.resolvedPassengerUrl.func.view_class,
                          PassengerView)

    def test_passengerDetailIsResolved(self):
        self.assertEquals(self.resolvedPassengerDetailUrl.func.view_class,
                          PassengerDetailView)

    def test_tripIsResolved(self):
        self.assertEquals(self.resolvedTripUrl.func.view_class,
                          TripView)

    def test_tripDetailIsResolved(self):
        self.assertEquals(self.resolvedTripDetailUrl.func.view_class,
                          TripDetailView)


class PassengerTest(APITestCase, PassengerTestBase):

    def setUp(self):
        self.client = APIClient()
        self.faker = Faker()
        self.passengerCount = 3
        self.tripCount = 6
        passengerList = []
        for _ in range(self.passengerCount):
            passengerList.append(Passenger.objects.create(firstName=self.faker.unique.first_name(),
                                                          lastName=self.faker.unique.last_name(),
                                                          email=self.faker.unique.email()))
        for _ in range(self.tripCount):
            Trip.objects.create(passenger=passengerList[random.randint(0, self.passengerCount-1)],
                                startTime=timezone.now(),
                                endTime=(timezone.now() + random.random() *
                                         timedelta(days=1)),
                                startLocation=self.faker.unique.city(),
                                endLocation=self.faker.city(),
                                totalDistance=random.uniform(0, 500))

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
        self.passengerCount = 3
        self.tripCount = 6
        passengerList = []
        for _ in range(self.passengerCount):
            passengerList.append(Passenger.objects.create(firstName=self.faker.unique.first_name(),
                                                          lastName=self.faker.unique.last_name(),
                                                          email=self.faker.unique.email()))
        for _ in range(self.tripCount):
            Trip.objects.create(passenger=passengerList[random.randint(0, self.passengerCount-1)],
                                startTime=timezone.now(),
                                endTime=(timezone.now() + random.random() *
                                         timedelta(days=1)),
                                startLocation=self.faker.unique.city(),
                                endLocation=self.faker.city(),
                                totalDistance=random.uniform(0, 500))

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
        self.assertEquals(responseGet.status_code,
                          status.HTTP_404_NOT_FOUND,
                          "Data is not deleted.")


class TripTest(APITestCase, TripTestBase):
    def setUp(self):
        self.client = APIClient()
        self.faker = Faker()
        self.passengerCount = 3
        self.tripCount = 6
        passengerList = []
        for _ in range(self.passengerCount):
            passengerList.append(Passenger.objects.create(firstName=self.faker.unique.first_name(),
                                                          lastName=self.faker.unique.last_name(),
                                                          email=self.faker.unique.email()))
        for _ in range(self.tripCount):
            Trip.objects.create(passenger=passengerList[random.randint(0, self.passengerCount-1)],
                                startTime=timezone.now(),
                                endTime=(timezone.now() + random.random() *
                                         timedelta(days=1)),
                                startLocation=self.faker.unique.city(),
                                endLocation=self.faker.unique.city(),
                                totalDistance=random.uniform(0, 500))

    def test_getAll(self):
        response = self.client.get(self.tripUrl)

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,
                          "Status Code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["trips", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertTrue(len(response.json()["trips"]) > 0,
                        "Returned no trips")
        self.assertEquals(response.json()["result"],
                          ResultTypes.RETRIEVED,
                          "Returned result value is not correct")

    def test_create(self):
        data = {"passenger": "1",
                "startTime": timezone.now(),
                "endTime": (timezone.now() + random.random() *
                            timedelta(days=1)),
                "startLocation": self.faker.unique.city(),
                "endLocation": self.faker.unique.city(),
                "totalDistance": random.uniform(0, 500)}
        response = self.client.post(self.tripUrl, data=data)

        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED,
                          "Status Code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["trips", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertEquals(response.json()["result"],
                          ResultTypes.CREATED,
                          "Returned result value is not correct.")


class TripDetailTest(APITestCase, TripTestBase):
    def setUp(self):
        self.client = APIClient()
        self.faker = Faker()
        self.passengerCount = 3
        self.tripCount = 6
        passengerList = []
        for _ in range(self.passengerCount):
            passengerList.append(Passenger.objects.create(firstName=self.faker.unique.first_name(),
                                                          lastName=self.faker.unique.last_name(),
                                                          email=self.faker.unique.email()))
        for _ in range(self.tripCount):
            Trip.objects.create(passenger=passengerList[random.randint(0, self.passengerCount-1)],
                                startTime=timezone.now(),
                                endTime=(timezone.now() + random.random() *
                                         timedelta(days=1)),
                                startLocation=self.faker.unique.city(),
                                endLocation=self.faker.city(),
                                totalDistance=random.uniform(0, 500))

    def test_get_one(self):
        response = self.client.get(self.tripDetailUrl)

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,
                          "Status Code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["trips", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertTrue('id' in response.json()["trips"].keys(),
                        "Returned trip object has no id key")
        self.assertEquals(response.json()["result"],
                          ResultTypes.RETRIEVED,
                          "Returned result value is not correct")

    def test_update(self):
        data = {"passenger": 1,
                "startTime": timezone.now().isoformat(),
                "endTime": (timezone.now() + random.random() *
                            timedelta(days=1)).isoformat(),
                "startLocation": self.faker.unique.city(),
                "endLocation": self.faker.unique.city(),
                "totalDistance": random.uniform(0, 500)}
        response = self.client.put(self.tripDetailUrl, data=data)

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK, "Status code is not correct")
        self.assertEquals(list(response.json().keys()),
                          ["trips", "result", "errorMessage"],
                          "Returned keys are not correct")
        self.assertTrue('id' in response.json()["trips"].keys(),
                        "Returned trip object has no id key")

    def test_delete(self):

        responseDel = self.client.delete(self.tripDetailUrl)
        responseGet = self.client.get(self.tripDetailUrl)

        self.assertEquals(responseDel.status_code,
                          status.HTTP_204_NO_CONTENT,
                          "Status code is not correct")
        self.assertEquals(responseDel.data["result"],
                          ResultTypes.DELETED,
                          "Returned result is not correct")
        self.assertEquals(responseGet.status_code,
                          status.HTTP_404_NOT_FOUND,
                          "Data is not deleted.")
