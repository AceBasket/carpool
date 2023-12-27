"""
URL Configuration for carpool_app
"""
from django.urls import path, include
from rest_framework import routers

from carpool_app import views

router = routers.DefaultRouter()
router.register(r'trips', views.TripViewSet)
router.register(r'registrations', views.TripRegistrationViewSet,
                basename='registration')
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'trips/<slug:slug>/trip-parts/',
        views.TripPartViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='trip_part-list'
    ),
    path(
        'trips/<slug:trip_slug>/trip-parts/<slug:slug>/',
        views.TripPartViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='trip_part-detail'
    ),
]
