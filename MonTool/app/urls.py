from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.signin, name="login"),
    path("logout/", views.logout, name="logout"),
    path("home/", views.home, name="home"),
    path("profile/", views.create_profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("add_server/", views.add_server, name="add_server"),
    path("<int:server_id>/", views.server_details, name="server_details"),
    path("my_servers/", views.my_servers, name="my_servers"),
    path("<int:server_id>/edit_server/", views.edit_server, name="edit_server"),
    path("<int:server_id>/delete_server/", views.delete_server, name="delete_server"),
    path('stop_monitoring/<int:server_id>/', views.stop_monitoring, name='stop_monitoring'),
    path('tg_integation/', views.tg_integration, name='tg_integration'),
]
