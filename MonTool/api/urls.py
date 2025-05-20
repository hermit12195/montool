from django.urls import path

from api.views import Signup, Login, AddServer, ListServers

urlpatterns = [
    path('api_signup/', Signup.as_view(), name="api_signup"),
    path("api_login/", Login.as_view(), name="api_login"),
    path("api_addserver/", AddServer.as_view(), name="api_addserver"),
    path("api_listservers/", ListServers.as_view(), name="api_listservers")
]
