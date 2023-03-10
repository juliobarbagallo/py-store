from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order, OrderProduct


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def get_cart_total(self):
        # Get the user's open order, if any
        open_order = self.get_open_order()
        if open_order:
            return open_order.get_order_total
        else:
            return 0

    @property
    def get_cart_items(self):
        # Get the user's open order, if any
        open_order = self.get_open_order()
        if open_order:
            return open_order.get_order_products
        else:
            return []

    def get_open_order(self):
        # Get the user's open order, or create one if none exists
        open_orders = Order.objects.filter(user=self.user, status="open")
        if open_orders.exists():
            return open_orders.first()
        else:
            new_order = Order.objects.create(user=self.user, status="open")
            return new_order

    def complete_order(self):
        # Complete the user's open order, if any
        open_order = self.get_open_order()
        if open_order:
            open_order.status = "complete"
            open_order.save()
