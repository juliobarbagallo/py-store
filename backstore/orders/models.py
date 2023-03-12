from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, through="OrderProduct", related_name="orders"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

    @property
    def get_order_products(self):
        order_items = self.orderproduct_set.all()
        return order_items

    @property
    def get_order_total(self):
        order_items = self.orderproduct_set.all()
        total = sum([item.get_total for item in order_items])
        return total


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
