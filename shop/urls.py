from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('product/<str:slug>', ViewProduct.as_view(), name="product"),
    path('brands', get_brands, name='brands'),
    path('catalog/<str:slug>', ProductsByCategory.as_view(), name="category"),
    path('catalog', ProductsCatalog.as_view(), name="catalog"),

    path('comments/add_comment', AddComment.as_view(), name="add_comment"),
    path('comments/toggle_comment_vote', ToggleCommentVote.as_view(), name="toggle_comment_vote"),
]
