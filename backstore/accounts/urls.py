from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("logout/", views.logout_view, name="logout"),
    # path("profile/", views.profile, name="profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("view_profile/", views.view_profile, name="view_profile"),
]
