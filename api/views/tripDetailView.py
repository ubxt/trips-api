from distutils.util import strtobool
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..standards import TripResponse, ResultTypes
from base.models import Trip
from ..serializers import TripSerializer, TripSerializerWithPassenger


class TripDetailView(APIView):

    def get_trip(self, id):
        try:
            return Trip.objects.get(id=id)
        except Trip.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    def get(self, request, id, format=None):
        trip = self.get_trip(id)
        isDetailed = request.query_params.get('detailed')
        if trip:
            serializedTrip = (TripSerializerWithPassenger(trip)
                              if (isDetailed and
                                  bool(strtobool(isDetailed)))
                              else TripSerializer(trip))
            returnObj = TripResponse(
                serializedTrip.data, ResultTypes.RETRIEVED)
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_200_OK)
        else:
            returnObj = TripResponse(
                None, ResultTypes.ERROR, "Not Found.")
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        trip = self.get_trip(id)
        if trip:
            serializer = TripSerializer(trip, data=request.data)
            if serializer.is_valid():
                serializer.save()
                returnObj = TripResponse(
                    serializer.data, ResultTypes.UPDATED)
                return Response(returnObj.to_json(), status=status.HTTP_200_OK)
            else:
                returnObj = TripResponse(
                    trips=None, result=ResultTypes.ERROR,
                    errorMessage="Data posted is not valid")
                return Response(returnObj.to_json(),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            returnObj = TripResponse(
                trips=None, result=ResultTypes.ERROR,
                errorMessage="Not found")
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        trip = self.get_trip(id)
        if trip:
            trip.delete()
            returnObj = TripResponse(trips=None,
                                     result=ResultTypes.DELETED)
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_204_NO_CONTENT)
        else:
            returnObj = TripResponse(trips=None,
                                     result=ResultTypes.ERROR,
                                     errorMessage="Not Found")
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_404_NOT_FOUND)
