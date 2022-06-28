
<img src="https://cdn-icons.flaticon.com/png/512/2915/premium/2915172.png?token=exp=1656457523~hmac=c427a5484facbe6b1d1f35c3d5c1e2e3" width=64 height=64 align=right>
<br>
<br>

# Trips API

A web API to make CRUD operations for a system that handles trips and passengers.
<br>
<br>

## Built using 

<img src=https://www.django-rest-framework.org/img/logo.png height=150 align=left >

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<img src=https://warehouse-camo.ingress.cmh1.psfhosted.org/b1336bf90c555ca9b45aca49e9d2b51a00783c1c/687474703a2f2f646f63732e63656c65727970726f6a6563742e6f72672f656e2f6c61746573742f5f696d616765732f63656c6572792d62616e6e65722d736d616c6c2e706e67>

<br>

## Installation

### Source code
```bash
    pip install -r requirements.txt
```

### Via Docker
```bash
    docker-compose up
```

## Endpoints
> ### Passenger
> - _GET_ /api/passenger : Returns all passengers <strong>*</strong>
> - _POST_ /api/passenger : Creates new passenger. Expects passenger object as json from request body.
> - _GET_ /api/passenger/< id > : Returns single passenger with the specified id <strong>*</strong>
> - _PUT_ /api/passenger/< id > : Updates the passenger with the specified id. Expects passenger object from body.
> - _DELETE_ /api/passenger/< id > : Deletes the passenger with the specified id.
> <br>
<br>

<br>

> ### Trip
> - _GET_ /api/passenger : Returns all trips <strong>*</strong>
> - _POST_ /api/passenger : Creates new trip. Expects trip object as json from request body.
> - _GET_ /api/passenger/< id > : Returns single passenger with the specified id <strong>*</strong>
> - _PUT_ /api/passenger/< id > : Updates the trip with the specified id. Expects trip object from body.
> - _DELETE_ /api/passenger/< id > : Deletes the trip with the specified id.
> <br>
<br>

<strong>[*] : GET endpoints can accept _detailed=< true | false >_ query parameter. This parameter controls whether the bound objects will be returned or not with the query.
</strong>

```
GET /api/passenger?detailed=true
```
will return passengers with their trip objects.

Similarly,
```
GET /api/trip?detailed=true
```
will return trips with their passenger objects.

## Models

> ### Passenger
> <i>firstName</i> : CharField(50) <br>
> <i>lastName</i> : CharField(50) <br>
> <i>email</i> : EmailField <br>
> <i>created</i> : DateTimeField  _(internal)_<br>
> <br>


> ### Trip
> <i>passenger</i> : ForeignKey <br>
>    startTime : DateTimeField <br>
>    endTime : DateTimeField <br>
>    startLocation : CharField(100) <br>
>    endLocation = CharField(100) <br>
>    totalDistance = FloatField(10)

