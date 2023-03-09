from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def get_cart_total(self):
        order_items = self.cart.orderproduct_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.cart.orderproduct_set.all()
        total_items = sum([item.quantity for item in order_items])
        return total_items


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_cart"
    )
    products = models.ManyToManyField(Product, blank=True, related_name="user_carts")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def get_cart_products(self):
        cart_items = self.cartproduct_set.all()
        return cart_items

    @property
    def get_cart_total(self):
        cart_items = self.cartproduct_set.all()
        total = sum([item.get_total for item in cart_items])
        return total


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
