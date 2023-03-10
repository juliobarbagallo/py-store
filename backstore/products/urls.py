from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("add/", views.add_product, name="add_product"),
    path("healthcheck/", views.health_check, name="health_check"),
    path("products/", views.products, name="products"),
]
