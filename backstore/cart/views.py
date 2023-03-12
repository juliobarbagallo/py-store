from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        quantity = int(request.POST["quantity"])
        cart_item, item_created = CartItem.objects.get_or_create(
            cart_item=cart, product=product
        )
        cart_item.quantity += quantity
        cart_item.save()
        return redirect("cart")

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
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.products.all()
    cart_total = cart.get_cart_total
    return render(
        request,
        "cart/cart_detail.html",
        {"cart_items": cart_items, "cart_total": cart_total},
    )
