from django.contrib import admin
from .models import Car, Trip, TripPart, TripRegistration

# Register your models here.
admin.site.register(Car)
admin.site.register(Trip)
admin.site.register(TripPart)
admin.site.register(TripRegistration)
