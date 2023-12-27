from django.db import models
from user.models import User


class Car(models.Model):
    """Car model"""
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=10, blank=True)
    num_passenger_seats = models.IntegerField()
    license_plate = models.CharField(max_length=10, unique=True)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='car')

    objects = models.Manager()

    def __str__(self):
        return str(self.license_plate)


class Trip(models.Model):
    """Trip model"""
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='trips')

    class Meta:
        """Meta class for Trip model"""
        unique_together = ('date', 'car')

    objects = models.Manager()

    def __str__(self):
        return str(self.id) + " on " + str(self.date)


class Review(models.Model):
    """Review model"""
    id = models.AutoField(primary_key=True)
    score = models.IntegerField()
    content = models.CharField(max_length=100, blank=True)
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_emited')
    reviewee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_received')
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='reviews')

    objects = models.Manager()

    def __str__(self):
        return str(self.id) + " " + str(self.score) + " from " + str(self.reviewer) + " to " + str(self.reviewee) + " on " + str(self.trip)


class TripRegistration(models.Model):
    """Sign up model"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='registrations')
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='registrations')

    objects = models.Manager()

    # class Meta:
    #     """Meta class for TripRegistration model"""
    #     constraints = [
    #         # limit trip registrations to number of seats in car
    #         models.CheckConstraint(
    #             check=models.Q(trip__car__num_passenger_seats__gte=models.Count(
    #                 'trip__registrations')),
    #             name='trip_registration_limit'
    #         ),
    #     ]

    def __str__(self):
        return str(self.id)


class TripPart(models.Model):
    """Trip part model"""
    id = models.AutoField(primary_key=True)
    departure_time = models.TimeField()
    distance = models.IntegerField()
    duration = models.IntegerField()
    fee = models.IntegerField()
    starting_point = models.CharField(max_length=20)
    ending_point = models.CharField(max_length=20)
    registrations = models.ManyToManyField(
        TripRegistration, related_name='trip_parts', blank=True)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='trip_parts')

    objects = models.Manager()

    # class Meta:
    #     """Meta class for TripPart model"""
    #     constraints = [
    #         # prohibit trip parts belonging to same trip with same starting or ending points
    #         models.CheckConstraint(check=models.Q(
    #             trip__trip_parts__starting_point__ne=models.F('starting_point')) & models.Q(trip__trip_parts__ending_point_ne=models.F('ending_point')), name='trip_part_starting_point'),
    #     ]

    def __str__(self):
        return self.starting_point + " to " + self.ending_point + " on " + str(self.trip)
