from django.db.models import Model, CharField, EmailField, DateTimeField


class Passenger(Model):
    firstName = CharField(max_length=50, verbose_name="First Name")
    lastName = CharField(max_length=50, verbose_name="Last Name")
    email = EmailField(max_length=100, verbose_name="Email")
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName
