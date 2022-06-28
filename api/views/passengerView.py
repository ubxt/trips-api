from distutils.util import strtobool
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..standards import PassengerResponse, ResultTypes
from base.models import Passenger
from ..serializers import PassengerSerializer, PassengerSerializerWithTrips
from api.tasks import create_passenger_email_task


class PassengerView(APIView):
    def get(self, request, format=None):
        passengers = Passenger.objects.all()
        isDetailed = request.query_params.get("detailed")
        if passengers:
            serializedPassengers = (
                PassengerSerializerWithTrips(passengers, many=True)
                if (isDetailed and bool(strtobool(isDetailed)))
                else PassengerSerializer(passengers, many=True)
            )
            returnObj = PassengerResponse(
                passengers=serializedPassengers.data, result=ResultTypes.RETRIEVED
            )
            return Response(data=returnObj.to_json(), status=status.HTTP_200_OK)
        else:
            returnObj = PassengerResponse(passengers=None, result=ResultTypes.NOT_FOUND)
            return Response(data=returnObj.to_json(), status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = PassengerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            returnObj = PassengerResponse(
                passengers=serializer.data, result=ResultTypes.CREATED
            )
            create_passenger_email_task.delay()
            return Response(returnObj.to_json(), status=status.HTTP_201_CREATED)
        else:
            returnObj = PassengerResponse(
                result=ResultTypes.ERROR, errorMessage="Data posted is not valid"
            )
            return Response(returnObj.to_json(), status=status.HTTP_400_BAD_REQUEST)
