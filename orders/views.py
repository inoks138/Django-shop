from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.shortcuts import render
from django.urls import reverse_lazy

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required(login_url=reverse_lazy('login'))
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()

            return render(request, 'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order.html',
                  {'cart': cart, 'form': form})
