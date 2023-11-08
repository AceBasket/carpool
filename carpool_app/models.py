from django.db import models

# Create your models here.


class People(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class Cars(models.Model):
    car_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    num_passenger_seats = models.IntegerField()
    license_plate = models.CharField(max_length=10)
    owner_id = models.ForeignKey(People, on_delete=models.CASCADE)


class Trips(models.Model):
    trip_id = models.AutoField(primary_key=True)
    date = models.DateField()
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)


class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    score = models.IntegerField()
    content = models.CharField(max_length=100)
    reviewer_id = models.ForeignKey(People, on_delete=models.CASCADE)
    reviewee_id = models.ForeignKey(People, on_delete=models.CASCADE)
    trip_id = models.ForeignKey(Trips, on_delete=models.CASCADE)


class Sign_Ups(models.Model):
    sign_up_id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(People, on_delete=models.CASCADE)
    trip_id = models.ForeignKey(Trips, on_delete=models.CASCADE)


class Trip_Parts(models.Model):
    trip_part_id = models.AutoField(primary_key=True)
    departure_time = models.TimeField()
    distance = models.IntegerField()
    duration = models.IntegerField()
    fee = models.IntegerField()
    starting_point = models.CharField(max_length=20)
    ending_point = models.CharField(max_length=20)
    trip_id = models.ForeignKey(Trips, on_delete=models.CASCADE)


class Trip_Part_Sign_Ups(models.Model):
    trip_part_id = models.ForeignKey(Trip_Parts, on_delete=models.CASCADE)
    sign_up_id = models.ForeignKey(Sign_Ups, on_delete=models.CASCADE)
