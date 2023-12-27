from django.contrib import admin
from .models import Car, Trip, TripPart, TripRegistration


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'num_passenger_seats',
                    'color', 'model', 'license_plate')
    prepopulated_fields = {'slug': ('license_plate',)}


# Register your models here.
admin.site.register(Car)
admin.site.register(Trip)
admin.site.register(TripPart)
admin.site.register(TripRegistration)
