from django.urls import path

from .views import AddCart, RemoveCart

urlpatterns = [
    path('add/<int:pk>', AddCart.as_view(), name="add_cart"),
    path('remove/<int:pk>', RemoveCart.as_view(), name="remove_cart"),
]
