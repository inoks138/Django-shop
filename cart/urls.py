from django.urls import path

from .views import *

urlpatterns = [
    path('add/<int:pk>', AddAjaxHandlerView.as_view(), name="add_cart"),
    path('remove/<int:pk>', RemoveAjaxHandlerView.as_view(), name="remove_cart"),
]