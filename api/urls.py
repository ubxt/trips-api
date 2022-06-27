from django.urls import path
from api.views.passengerView import PassengerView
from api.views.passengerDetailView import PassengerDetailView

urlpatterns = [
    # path('', home, name="Home"),
    path('passenger/', PassengerView.as_view(), name="passenger"),
    path('passenger/<int:id>', PassengerDetailView.as_view(),
         name="passengerDetail")
]
