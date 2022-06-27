from django.urls import path
# from api.views import home
from api.views.passengerView import PassengerView

urlpatterns = [
    # path('', home, name="Home"),
    path('passenger/', PassengerView.as_view(), name="passenger"),
    # path('passenger/<int:id>', get_all, name="passenger_with_id")
]
