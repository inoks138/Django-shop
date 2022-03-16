from django.urls import path

from .views import register, account_login, account_logout

urlpatterns = [
    path('register', register, name="register"),
    path('login', account_login, name="login"),
    path('logout/', account_logout, name='logout'),
]