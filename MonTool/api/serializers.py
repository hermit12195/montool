import os

from cryptography.fernet import Fernet
from django.contrib.auth import authenticate
from rest_framework import serializers
import logging

from app.models import MonUser, Server

fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

logger = logging.getLogger("api")


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles creation of a new MonUser with a hashed password.
    Logs errors during the creation process.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = MonUser
        fields = ("email", "password")

    def create(self, validated_data):
        """
        Creates and returns a new MonUser instance.
        """
        try:
            user = MonUser.objects.create(email=validated_data["email"])
            user.set_password(validated_data["password"])
            user.save()
            return user
        except Exception as error:
            logger.error(f"Signup Serializer: {error}")


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Validates user credentials and returns the authenticated user.
    Logs errors during validation or creation.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validates user credentials and attaches the user object to attrs.
        """
        try:
            user = authenticate(email=attrs["email"], password=attrs["password"])
            if not user:
                raise serializers.ValidationError("Invalid credentials!")
            attrs["user"] = user
            return attrs
        except Exception as error:
            logger.error(f"Login Serializer: {error}")

    def create(self, validated_data):
        """
        Returns the authenticated user from validated_data.
        """
        try:
            return validated_data["user"]
        except Exception as error:
            logger.error(f"Login Serializer: {error}")


class AddServerSerializer(serializers.ModelSerializer):
    """
    Serializer for adding a new server.

    Encrypts the server password before saving.
    Logs errors during the creation process.
    """

    class Meta:
        model = Server
        fields = ("server_name", "user_name", "server_ip", "password", "os_name")

    def create(self, validated_data):
        """
        Encrypts the password and creates a new Server instance.
        """
        try:
            validated_data["password"] = fernet.encrypt(validated_data["password"].encode()).decode()
            return Server.objects.create(**validated_data)
        except Exception as error:
            logger.error(f"AddServer Serializer: {error}")


class ListServersSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all server records.
    """

    class Meta:
        model = Server
        fields = "__all__"
