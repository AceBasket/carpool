from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Q


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class TripManager(models.Manager):
    """
    Custom Trip model manager
    """

    def get_queryset(self):
        """
        Fetch related trip parts
        """
        return super().get_queryset().prefetch_related("trip_parts")

    def get_by_source_and_destination(self, source=None, destination=None):
        """
        Fetch trips by source and destination
        """
        return super().get_queryset().filter(Q(trip_parts__starting_point=source) & Q(trip_parts__ending_point=destination))

class reviewManager(models.Manager):
    """
    Custom review model manager
    """

    def get_queryset(self):
        """
        Fetch related trip parts
        """
        return super().get_queryset().prefetch_related("reviewer_id")

    def get_by_source_and_destination(self, source=None, destination=None):
        """
        Fetch trips by source and destination
        """
        return super().get_queryset().filter(Q(trip_parts__starting_point=source) & Q(trip_parts__ending_point=destination))