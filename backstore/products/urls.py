from django.urls import path
from . import views
from cart.views import add_to_cart
from .views import Ping, ProductList

app_name = "products"

urlpatterns = [
    path("add/", views.add_product, name="add_product"),
    path("healthcheck/", views.health_check, name="health_check"),
    path("products/", views.products, name="products"),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("api/products/", ProductList.as_view(), name="api_products"),
    path("api/ping/", Ping.as_view(), name="api_ping"),
]
