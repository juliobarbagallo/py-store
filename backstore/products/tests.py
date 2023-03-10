from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category
from products.forms import ProductForm


class HealthCheckViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("products:health_check")

    def test_health_check_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hello from products")


class ProductViewTestCase(TestCase):
    def test_product_added(self):
        before_count = Product.objects.count()
        self.category = Category.objects.create(name="test cat")

        form_data = {
            "name": "Product from tests",
            "price": 10,
            "stock": 10,
            "image_url": "https://example.com/image.jpg",
            "description": "TESTDESC",
            "category": self.category.id,
        }
        response = self.client.post(reverse("products:add_product"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), before_count + 1)

        response = self.client.get(reverse("products:products"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product from tests")

        new_product = Product.objects.order_by("-id").first()
        self.assertEqual(new_product.name, "Product from tests")
        self.assertEqual(new_product.price, 10)
        self.assertEqual(new_product.stock, 10)
        self.assertEqual(new_product.image_url, "https://example.com/image.jpg")
        self.assertEqual(new_product.description, "TESTDESC")
        self.assertEqual(new_product.category, self.category)

        self.assertEqual(new_product.category.name, "test cat")

        self.assertGreater(new_product.id, before_count)
