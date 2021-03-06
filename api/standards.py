
class ResultTypes:
    CREATED = "created"
    NOT_FOUND = "Not Found"
    RETRIEVED = "retrieved"
    ERROR = "Error"
    UPDATED = "Updated"
    DELETED = "Deleted"


class PassengerResponse:
    def __init__(self, passengers: dict = None,
                 result: str = None,
                 errorMessage: str = None):
        self.passengers = passengers
        self.result = result
        self.errorMessage = errorMessage

    def to_json(self):
        return self.__dict__


class TripResponse:
    def __init__(self, trips: dict = None,
                 result: str = None,
                 errorMessage: str = None):
        self.trips = trips
        self.result = result
        self.errorMessage = errorMessage

    def to_json(self):
        return self.__dict__
