from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
]
