from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product


def index(request):
    return render(request, 'shop/index.html')


class ViewProduct(DetailView):
    model = Product
    context_object_name = 'product'
    allow_empty = False


def get_brand(request, slug):
    return HttpResponse(f"<h3>Бренд - {slug}</h3>")


def get_category(request, slug):
    return HttpResponse(f"<h3>Категория - {slug}</h3>")


def get_catalog(request):
    return HttpResponse(f"<h3>Каталог</h3>")
