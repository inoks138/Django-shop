from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Product, Category


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


class ProductsCatalog(ListView):
    model = Product
    template_name = 'shop/catalog.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(level__in=[0, 1])
        return context
