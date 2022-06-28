from django.urls import path
from api.views.passengerView import PassengerView
from api.views.passengerDetailView import PassengerDetailView
from api.views.tripView import TripView
from api.views.tripDetailView import TripDetailView

urlpatterns = [
    # path('', home, name="Home"),
    path('passenger/', PassengerView.as_view(), name="passenger"),
    path('passenger/<int:id>', PassengerDetailView.as_view(),
         name="passengerDetail"),
    path('trip/', TripView.as_view(), name="trip"),
    path('trip/<int:id>', TripDetailView.as_view(), name="tripDetail")
]
