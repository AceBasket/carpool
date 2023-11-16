from rest_framework import routers
from carpool_app import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'trip-parts', views.TripPartViewSet)
router.register(r'registrations', views.TripRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
