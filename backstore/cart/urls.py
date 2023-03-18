from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("clean_cart", views.clean_cart, name="clean_cart"),
    path("remove/<int:item_id>", views.remove_from_cart, name="remove_from_cart"),
]
