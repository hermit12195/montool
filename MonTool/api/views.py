from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import SignupSerializer, LoginSerializer, AddServerSerializer, ListServersSerializer
from app.models import Server
import logging

logger = logging.getLogger("api")


class AuthMixin(CreateAPIView):
    """
    Mixin to handle user authentication and token creation.
    Used by Signup and Login views.
    """

    def perform_create(self, serializer):
        """
        Saves the user and generates an auth token.
        """
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        self.token = token

    def create(self, request, *args, **kwargs):
        """
        Returns a response containing the user's token.
        """
        super().create(request, *args, **kwargs)
        return Response(data={"token": self.token.key}, status=self.status)


class Signup(AuthMixin):
    """
    API view for user signup.
    """
    serializer_class = SignupSerializer
    status = status.HTTP_201_CREATED
    logger.info("User is created")


class Login(AuthMixin):
    """
    API view for user login.
    """
    serializer_class = LoginSerializer
    status = status.HTTP_200_OK
    logger.info("User is logged in")


class AddServer(CreateAPIView):
    """
    API view to add a new server.
    Requires user to be authenticated.
    """
    serializer_class = AddServerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates the server with the authenticated user.
        """
        serializer.save(owner=self.request.user)
        logger.info("Server is added")


class ListServers(ListAPIView):
    """
    API view to list all servers for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ListServersSerializer

    def get_queryset(self):
        """
        Filters servers by the authenticated user.
        """
        logger.info("Servers are listed")
        return Server.objects.filter(owner=self.request.user)
