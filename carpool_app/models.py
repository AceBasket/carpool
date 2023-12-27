from django.db import models
from django.urls import reverse
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
    slug = models.SlugField(null=False, blank=False, unique=True)

    def __str__(self):
        return f"Car {self.license_plate}"

    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'slug': self.slug})


class Trip(models.Model):
    """Trip model"""
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='trips')
    slug = models.SlugField(null=False, blank=False,
                            unique=True, max_length=255)

    class Meta:
        """Meta class for Trip model"""
        unique_together = ('date', 'car')

    def __str__(self):
        return f" Trip with {self.car} on {self.date}"

    def get_absolute_url(self):
        return reverse('trip_detail', kwargs={'slug': self.slug})


class TripRegistration(models.Model):
    """Sign up model"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='registrations')
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='registrations')
    slug = models.SlugField(null=False, blank=False,
                            unique=True, max_length=255)

    def __str__(self):
        return f"Registration of user {self.user} for ({self.trip})"

    def get_absolute_url(self):
        return reverse('trip_registration_detail', kwargs={'slug': self.slug})


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
    slug = models.SlugField(null=False, blank=False,
                            unique=True, max_length=255)

    def __str__(self):
        return f"Trip part from {self.starting_point} to {self.ending_point} of {self.trip}"

    def get_absolute_url(self):
        return reverse('trip_part_detail', kwargs={'slug': self.slug})
