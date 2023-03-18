import logging
import os
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

from django.core.cache import cache
import json
import redis
from django.conf import settings

app_name = "products"
log_file_path = f"{app_name}/{app_name}.out"
log_level = logging.DEBUG
logger = configure_logger(log_file_path, log_level)


class Ping(APIView):
    def get(self, request, format=None):
        return Response({"message": "pong"})


# class ProductList(APIView):
#     def get(self, request, format=None):

#         r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=os.getenv("REDIS_DB"))
#         product_list = r.get('product_list')
#         if product_list:
#             # If the product list is in Redis, return it
#             products = json.loads(product_list)
#         else:
#             # If the product list is not in Redis, query the database and cache the result
#             products = Product.objects.all()
#             serializer = ProductSerializer(products, many=True)
#             products = serializer.data
#             r.set('product_list', json.dumps(products))

#         return Response(products)


class ProductList(APIView):
    def get(self, request, format=None):
        try:
            r = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                db=os.getenv("REDIS_DB"),
            )
            product_list = r.get("product_list")
            if product_list:
                logger.debug("Products are on redis.")
                products = json.loads(product_list)
            else:
                logger.debug("Products are not on redis.")
                products = Product.objects.all()
                serializer = ProductSerializer(products, many=True)
                products = serializer.data
                r.set("product_list", json.dumps(products))
        except redis.ConnectionError as e:
            # If there was an error connecting to Redis, log a warning and fallback to the database
            logging.warning(f"Redis connection error: {e}")
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            products = serializer.data

        return Response(products)


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
