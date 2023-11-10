from django.contrib.auth.models import Group
from rest_framework import serializers
from carpool_app.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for User model"""
    class Meta:
        """Meta class for UserSerializer"""
        model = User
        fields = ['id', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Group model"""
    class Meta:
        """Meta class for GroupSerializer"""
        model = Group
        fields = ['url', 'name']
