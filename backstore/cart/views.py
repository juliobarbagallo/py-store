import logging
from django.urls import reverse
from utils.logging_config import configure_logger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


app_name = "cart"
log_file_path = f"{app_name}/{app_name}.out"
log_level = logging.DEBUG
logger = configure_logger(log_file_path, log_level)


@login_required
def add_to_cart(request, product_id):
    logger.info("add_to_cart() was called")
    product = Product.objects.get(id=product_id)
    logger.debug(f"{product=}")
    cart, created = Cart.objects.get_or_create(user=request.user)
    logger.debug(f"{cart=}")

    if request.method == "POST":
        quantity = int(request.POST["quantity"])
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            logger.debug(f"CartItem {cart_item.id} already exists")
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=quantity
            )
            logger.debug(f"Creating new cart item")

        cart_item.quantity += quantity
        cart_item.save()

        logger.debug(f"Added {quantity} of {product.name} to cart")
        return redirect(reverse("products:products"))

    return render(request, "add_to_cart.html", {"product": product})


@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart.products.remove(product)
    messages.success(request, f"{product.name} removed from cart.")
    return redirect("cart:cart_detail")


@login_required
def clean_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.products.clear()
    messages.success(request, "Cart cleaned.")
    return redirect("cart:cart_detail")


@login_required
def cart_detail(request):
    logging.info("cart_detail() was called.")
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.get_cart_items
    cart_total = cart.get_cart_total
    logging.debug(f"{cart=} - {cart_items=} - {cart_total=}")
    return render(
        request,
        "cart_detail.html",
        {"cart_items": cart_items, "cart_total": cart_total},
    )
