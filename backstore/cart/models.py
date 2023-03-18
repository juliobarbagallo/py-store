from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def get_cart_items(self):
        return self.items.all()

    @property
    def get_cart_total(self):
        cart_items = self.items.all()
        total = sum([item.get_total for item in cart_items])
        return total


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        "Cart", related_name="items", on_delete=models.CASCADE, default=1
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.cart.user.username}"

    @property
    def get_total(self):
        return self.quantity * self.product.price
