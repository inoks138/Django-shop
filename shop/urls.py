from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('product/<str:slug>', get_product, name="product"),
    path('brand/<str:slug>', get_brand, name="brand"),
    path('catalog/<str:slug>', get_category, name="category"),
    path('catalog', get_catalog, name="catalog")
]
