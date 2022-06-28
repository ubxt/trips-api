from rest_framework.serializers import ModelSerializer
from base.models import Passenger, Trip


class PassengerSerializer(ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'firstName', 'lastName', 'email']


class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'passenger', 'startTime', 'endTime',
                  'startLocation', 'endLocation', 'totalDistance']


class PassengerSerializerWithTrips(ModelSerializer):
    trips = TripSerializer(many=True, read_only=True)

    class Meta:
        model = Passenger
        fields = ['id', 'firstName', 'lastName', 'email', 'trips']


class TripSerializerWithPassenger(ModelSerializer):

    class Meta:
        model = Trip
        depth = 1
        fields = ['id', 'passenger', 'startTime', 'endTime',
                  'startLocation', 'endLocation', 'totalDistance']
