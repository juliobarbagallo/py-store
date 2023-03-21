from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderProduct
from .forms import OrderForm


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = cart.get_cart_total
            order.status = "pending"  # Set the status to 'pending'
            order.save()
            for item in cart.items.all():
                OrderProduct.objects.create(
                    order=order, product=item.product, quantity=item.quantity
                )
            cart.items.all().delete()
            messages.success(request, "Your order has been placed!")
            return redirect("order_detail", order_id=order.id)
    else:
        form = OrderForm()
    return render(request, "order_create.html", {"form": form})
