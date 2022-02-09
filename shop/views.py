from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'shop/index.html')


def get_product(request, slug):
    return HttpResponse(f"<h3>Товар - {slug}</h3>")


def get_brand(request, slug):
    return HttpResponse(f"<h3>Бренд - {slug}</h3>")


def get_category(request, slug):
    return HttpResponse(f"<h3>Категория - {slug}</h3>")


def get_catalog(request):
    return HttpResponse(f"<h3>Каталог</h3>")
