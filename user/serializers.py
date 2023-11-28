from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        """Meta class for UserSerializer"""
        model = User
        fields = ['id', 'email', 'groups', 'password', 'otp_enabled',
                  'otp_verified', 'otp_base32', 'otp_auth_url']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.email = instance.email.lower()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model"""
    class Meta:
        """Meta class for GroupSerializer"""
        model = Group
        fields = ['url', 'name']
