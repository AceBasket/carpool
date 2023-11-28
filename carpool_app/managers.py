from django.db import models
from django.db.models import Q


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


class ReviewManager(models.Manager):
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
