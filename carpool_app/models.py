from django.db import models

# Create your models here.
class Cars(models.Model):
    car_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    num_passenger_seats = models.IntegerField()
    license_plate = models.CharField(max_length=10)
    owner_id = models.ForeignKey(People, on_delete=models.CASCADE)

class People(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)