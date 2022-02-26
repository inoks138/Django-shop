from django.shortcuts import get_object_or_404
from django.views import View
from shop.models import Product
from .cart import Cart
from django.http import HttpResponse, JsonResponse


class AddAjaxHandlerView(View):
    def get(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        cart.add(product)

        return JsonResponse({
            'pk': product.pk,
            'title': product.title,
            'slug': product.slug,
            'brand': product.brand.title,
            'photo': product.photo.url,
            'price': product.price,
            'absolute_url': product.get_absolute_url(),
            'quantity': cart.cart[str(product.id)]['quantity'],
            'total_it_price': cart.cart[str(product.id)]['quantity'] * product.price,
        }, status=200)


class RemoveAjaxHandlerView(View):
    def get(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        cart.remove(product)
        return HttpResponse('normalno', status=200)
