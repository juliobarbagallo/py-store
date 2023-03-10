from django.shortcuts import render, redirect
from .forms import ProductForm
from django.http import HttpResponse
from .models import Product
from django.urls import reverse

# Create your views here.


def products(request):
    products = Product.objects.all()
    return render(request, "products_list.html", {"products": products})


def add_product(request):
    print("add_product() called")
    if request.method == "POST":
        form = ProductForm(request.POST)
        print("FORM: ", form)
        if form.is_valid():
            print("Everything was ok!")
            form.save()
            return redirect(reverse("products:products"))
        print("Something is wrong!")
    else:
        print("form = ProductForm()")
        form = ProductForm()
    print("the retun statement")
    return render(request, "add_product.html", {"form": form})


def health_check(request):
    data = {"msg": "hello from products"}
    # return HttpResponse(content=data, content_type="application/json")
    return render(request, "health_check.html", context=data)
