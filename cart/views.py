from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from shop.models import Product
from .cart import Cart
from django.http import JsonResponse


class AddCart(View):
    def post(self, request, pk):
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
            'total_price': cart.get_total_price(),
            'remove_cart_url': reverse('remove_cart', kwargs={'pk': product.pk}),
        }, status=200)


class RemoveCart(View):
    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        cart.remove(product)
        return JsonResponse({
            'total_price': cart.get_total_price(),
            'slug': product.slug,
        }, status=200)
