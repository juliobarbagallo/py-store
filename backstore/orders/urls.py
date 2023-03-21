from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "orders"

urlpatterns = [
    path("order_create/", views.order_create, name="order_create"),
    path("order_list/", views.order_list, name="order_list"),
]
