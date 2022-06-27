from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..standards import PassengerResponse, ResultTypes
from base.models import Passenger
from ..serializers import PassengerSerializer


class PassengerView(APIView):

    def get(self, request, format=None):
        passengers = Passenger.objects.all()
        serializedPassengers = PassengerSerializer(passengers, many=True)
        returnObj = PassengerResponse(
            passengers=serializedPassengers.data, result=ResultTypes.RETRIEVED)
        return Response(data=returnObj.to_json(), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PassengerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            returnObj = PassengerResponse(
                passengers=serializer.data, result=ResultTypes.CREATED)
            return Response(returnObj.to_json(),
                            status=status.HTTP_201_CREATED)
        else:
            returnObj = PassengerResponse(
                result=ResultTypes.ERROR,
                errorMessage="Data posted is not valid")
            return Response(returnObj.to_json(),
                            status=status.HTTP_400_BAD_REQUEST)
