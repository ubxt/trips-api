from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..standards import standard_return_dict_passenger
from base.models import Passenger
from ..serializers import PassengerSerializer


class PassengerDetailView(APIView):

    def get_passenger(self, id):
        try:
            return Passenger.objects.get(id)
        except Passenger.DoesNotExist:
            return None

    def get(self, request, id, format=None):
        returnDict = standard_return_dict_passenger
        passenger = self.get_passenger(id)
        if passenger:
            serializedPassenger = PassengerSerializer(passenger)
            returnDict["passengers"] = serializedPassenger.data
            returnDict["result"] = "retrieved"
            return Response(data=returnDict, status=status.HTTP_200_OK)
        else:
            returnDict["result"] = "error"
            returnDict["errorMessage"] = "Not found"
            return Response(data=returnDict, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        returnDict = standard_return_dict_passenger
        passenger = self.get_passenger(id)
        if passenger:
            serializer = PassengerSerializer(passenger, data=request.data)
            if serializer.is_valid():
                serializer.save()
                returnDict["passengers"] = serializer.data
                returnDict["result"] = "updated"
                return Response(returnDict, status=status.HTTP_200_OK)
            else:
                returnDict["result"] = "error"
                returnDict["errorMessage"] = "Data posted is not valid"
                return Response(returnDict, status=status.HTTP_400_BAD_REQUEST)
        else:
            returnDict["result"] = "error"
            returnDict["errorMessage"] = "Not found"
            return Response(data=returnDict, status=status.HTTP_404_NOT_FOUND)
