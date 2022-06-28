from distutils.util import strtobool
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..standards import PassengerResponse, ResultTypes
from base.models import Passenger
from ..serializers import PassengerSerializer, PassengerSerializerWithTrips


class PassengerDetailView(APIView):

    def get_passenger(self, id):
        try:
            return Passenger.objects.get(id=id)
        except Passenger.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    def get(self, request, id, format=None):
        passenger = self.get_passenger(id)
        isDetailed = request.query_params.get('detailed')
        if passenger:
            serializedPassenger = (PassengerSerializerWithTrips(passenger)
                                   if (isDetailed and
                                       bool(strtobool(isDetailed)))
                                   else PassengerSerializer(passenger))
            returnObj = PassengerResponse(
                serializedPassenger.data, ResultTypes.RETRIEVED)
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_200_OK)
        else:
            returnObj = PassengerResponse(
                None, ResultTypes.ERROR, "Not Found.")
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        passenger = self.get_passenger(id)
        if passenger:
            serializer = PassengerSerializer(passenger, data=request.data)
            if serializer.is_valid():
                serializer.save()
                returnObj = PassengerResponse(
                    serializer.data, ResultTypes.UPDATED)
                return Response(returnObj.to_json(), status=status.HTTP_200_OK)
            else:
                returnObj = PassengerResponse(
                    passengers=None, result=ResultTypes.ERROR,
                    errorMessage="Data posted is not valid")
                return Response(returnObj.to_json(),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            returnObj = PassengerResponse(
                passengers=None, result=ResultTypes.ERROR,
                errorMessage="Not found")
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        passenger = self.get_passenger(id)
        if passenger:
            passenger.delete()
            returnObj = PassengerResponse(passengers=None,
                                          result=ResultTypes.DELETED)
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_204_NO_CONTENT)
        else:
            returnObj = PassengerResponse(passengers=None,
                                          result=ResultTypes.ERROR,
                                          errorMessage="Not Found")
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_404_NOT_FOUND)
