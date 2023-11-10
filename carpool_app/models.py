from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.


class User(AbstractUser):
    """Custom user model"""
    username = None
    email = models.EmailField(("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Car(models.Model):
    """Car model"""
    car_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=10, blank=True)
    num_passenger_seats = models.IntegerField()
    license_plate = models.CharField(max_length=10, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.license_plate)


class Trip(models.Model):
    """Trip model"""
    trip_id = models.AutoField(primary_key=True)
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.trip_id) + " on " + str(self.date)


class Review(models.Model):
    """Review model"""
    review_id = models.AutoField(primary_key=True)
    score = models.IntegerField()
    content = models.CharField(max_length=100, blank=True)
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewer_id')
    reviewee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewee_id')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.review_id) + " " + str(self.score) + " from " + str(self.reviewer) + " to " + str(self.reviewee) + " on " + str(self.trip)


class TripRegistration(models.Model):
    """Sign up model"""
    trip_registration_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.trip_registration_id)


class TripPart(models.Model):
    """Trip part model"""
    trip_part_id = models.AutoField(primary_key=True)
    departure_time = models.TimeField()
    distance = models.IntegerField()
    duration = models.IntegerField()
    fee = models.IntegerField()
    starting_point = models.CharField(max_length=20)
    ending_point = models.CharField(max_length=20)
    registrations = models.ManyToManyField(
        TripRegistration, related_name='trip_parts')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return self.starting_point + " to " + self.ending_point + " on " + str(self.trip)
