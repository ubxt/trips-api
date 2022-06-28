from django.db.models import (Model, CharField, EmailField,
                              DateTimeField, ForeignKey, CASCADE,
                              FloatField)


class Passenger(Model):
    firstName = CharField(max_length=50, verbose_name="First Name")
    lastName = CharField(max_length=50, verbose_name="Last Name")
    email = EmailField(max_length=100, verbose_name="Email")
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName


class Trip(Model):
    passenger = ForeignKey(Passenger,
                           on_delete=CASCADE, default=0, null=False,
                           verbose_name="Passenger ID", related_name="trips")
    startTime = DateTimeField(verbose_name='Start Time')
    endTime = DateTimeField(verbose_name='End Time')
    startLocation = CharField(max_length=100, verbose_name="Start Location")
    endLocation = CharField(max_length=100, verbose_name="End Location")
    totalDistance = FloatField(max_length=10, verbose_name="Total Distance")

    def __str__(self):
        return f"{self.passenger} | {self.startTime}-{self.endTime} | \
            {self.startLocation}-{self.endLocation}"
