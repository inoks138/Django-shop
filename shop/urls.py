from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('product/<str:slug>', ViewProduct.as_view(), name="product"),
    path('brand/<str:slug>', get_brand, name="brand"),
    path('brands', get_brands, name='brands'),
    path('catalog/<str:slug>', ProductsByCategory.as_view(), name="category"),
    path('catalog', ProductsCatalog.as_view(), name="catalog")
]
