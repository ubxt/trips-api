from distutils.util import strtobool
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..standards import ResultTypes, TripResponse
from base.models import Trip
from ..serializers import TripSerializer, TripSerializerWithPassenger


class TripView(APIView):

    def get(self, request, format=None):
        trips = Trip.objects.all()
        isDetailed = request.query_params.get('detailed')
        if trips:
            serializedTrips = (TripSerializerWithPassenger(trips, many=True)
                               if isDetailed and bool(strtobool(isDetailed))
                               else TripSerializer(trips, many=True))
            returnObj = TripResponse(
                trips=serializedTrips.data,
                result=ResultTypes.RETRIEVED)
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_200_OK)
        else:
            returnObj = TripResponse(
                trips=None, result=ResultTypes.NOT_FOUND)
            return Response(data=returnObj.to_json(),
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = TripSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            returnObj = TripResponse(
                trips=serializer.data, result=ResultTypes.CREATED)
            return Response(returnObj.to_json(),
                            status=status.HTTP_201_CREATED)
        else:
            returnObj = TripResponse(
                result=ResultTypes.ERROR,
                errorMessage="Data posted is not valid")
            return Response(returnObj.to_json(),
                            status=status.HTTP_400_BAD_REQUEST)
