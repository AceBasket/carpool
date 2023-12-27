from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    """Custom user model"""
    username = None
    email = models.EmailField(("email address"), unique=True)
    otp_enabled = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=255, null=True)
    otp_auth_url = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def is_2fa_enabled(self):
        """Returns True if 2FA is enabled for the user"""
        return self.otp_enabled
