import logging
from utils.logging_config import configure_logger
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.http import HttpResponse
from .models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer

app_name = "products"
log_file_path = f"{app_name}/{app_name}.out"
log_level = logging.DEBUG
logger = configure_logger(log_file_path, log_level)


class Ping(APIView):
    def get(self, request, format=None):
        return Response({"message": "pong"})


class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@login_required
def products(request):
    logger.info("products() was called.")
    logger.debug(f"{request=} - {request.body=} - {request.POST=}")
    products = Product.objects.all()
    return render(request, "products_list.html", {"products": products})


def add_product(request):
    logger.info("add_product() was called.")
    logger.debug(f"{request=} - {request.POST=}")
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("products:products"))
        logger.error("The form is not valid.")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})


def health_check(request):
    logger.info("health_check() was called.")
    data = {"msg": "hello from products"}
    # return HttpResponse(content=data, content_type="application/json")
    return render(request, "health_check.html", context=data)
