from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField("CartItem", blank=True, related_name="cart")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def get_cart_items(self):
        return self.cartitem_set.all()

    @property
    def get_cart_total(self):
        cart_items = self.cartitem_set.all()
        total = sum([item.get_total for item in cart_items])
        return total


class CartItem(models.Model):
    cart_item = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.cart.user.username}"

    @property
    def get_total(self):
        return self.quantity * self.product.price
