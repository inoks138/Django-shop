from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Product, Category, Brand


def index(request):
    return render(request, 'shop/index.html')


class ViewProduct(DetailView):
    model = Product
    context_object_name = 'product'
    allow_empty = False


def get_brand(request, slug):
    return HttpResponse(f"<h3>Бренд - {slug}</h3>")


class ProductsByCategory(DetailView):
    model = Category
    template_name = 'shop/catalog_category.html'
    context_object_name = 'category'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['ancestors_tree'] = context['category'].get_ancestors(include_self=True)
        return context


class ProductsCatalog(ListView):
    model = Product
    template_name = 'shop/catalog.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(level__in=[0, 1])
        context['brands'] = Brand.objects.all()
        if 'brands' in self.request.GET:
            brands = self.request.GET['brands'].split(',')
            context['products'] = context['products'].filter(brand__slug__in=brands)
        return context


def get_brands(request):
    return render(request, 'shop/brands.html')
