from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models


def user_photo_path(instance: 'Profile', filename: str) -> str:
    """
    Returns the upload path for a user's profile photo.
    """
    return f'user_{instance.user.id}/{filename}'


class MonUser(AbstractUser):
    """
    Custom user model using email instead of username.
    """
    username = None
    email: str = models.EmailField(unique=True, validators=[EmailValidator])
    tg_id: int = models.IntegerField(blank=True, null=True)
    tg_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Returns the string representation of the user.
        """
        return self.email


class Server(models.Model):
    """
    Model representing a monitored server.
    """
    server_name = models.CharField(max_length=120)
    user_name = models.CharField(max_length=120)
    server_ip = models.GenericIPAddressField(protocol='IPv4')
    password = models.CharField(max_length=120)
    os_name = models.CharField(max_length=120, default="Linux")
    status = models.CharField(max_length=120, default="online", null=True, blank=True)
    owner = models.ForeignKey(MonUser, on_delete=models.DO_NOTHING, related_name="servers")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """
        Returns the server name as string representation.
        """
        return self.server_name


class Profile(models.Model):
    """
    User profile model.
    """
    user = models.OneToOneField(MonUser, on_delete=models.CASCADE, related_name="profiles", null=True)
    first_name: Optional[str] = models.CharField(max_length=50, null=True)
    last_name: Optional[str] = models.CharField(max_length=50, null=True)
    bio: str = models.TextField(default="No bio yet!")
    birth_date: models.DateField = models.DateField()
    photo: models.ImageField = models.ImageField(upload_to=user_photo_path, default='default.png', blank=True)

    def __str__(self) -> str:
        """
        Returns the first name of the profile owner.
        """
        return self.first_name
