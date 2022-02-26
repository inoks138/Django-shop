from django import template
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from cart.cart import Cart

register = template.Library()


@register.inclusion_tag('cart/cart_tpl.html', takes_context=True)
def show_cart(context):
    request = context['request']
    cart = Cart(request)
    return {'cart': cart}


@register.simple_tag(takes_context=True)
def cart_add_product(context, product_id, quantity=1, update_quantity=False):
    request = context['request']
    cart = Cart(request)
    cart.add(product_id, quantity, update_quantity)
