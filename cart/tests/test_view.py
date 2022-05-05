import json
import tempfile

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from slugify import slugify

from account.models import Account
from cart.templatetags.cart_tags import cart_add_product
from shop.models import Product, Category, Brand


class CartTest(TestCase):

    def setUp(self):
        brand = Brand.objects.create(title='Крутой бренд', slug=slugify('Крутой бренд'))
        category = Category.objects.create(title='Крутая категория', slug=slugify('krutaia-kategoriia'))
        self.product1 = Product.objects.create(title=f'Крутой товар 1', slug=f'krutoi-tovar-1', category=category,
                                               brand=brand, photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                               price=200, stock=20)
        self.product2 = Product.objects.create(title=f'Крутой товар 2', slug=f'krutoi-tovar-2', category=category,
                                               brand=brand, photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                               price=300, stock=30)

        Account.objects.create(username="user", password="12345")
        self.client.login(username="user", password="12345")
        self.session = self.client.session

        self.session.update({
            settings.CART_SESSION_ID: {
                '1': {
                    'quantity': 2,
                    'price': '200.00',
                },
                '2': {
                    'quantity': 2,
                    'price': '300.00',
                },
            },
        })
        self.session.save()

    def test_cart_add_view(self):
        response = self.client.post(reverse('add_cart', kwargs={'pk': self.product1.pk}))
        data = json.loads(response.content)
        expected_data = {
            'pk': 1,
            'title': 'Крутой товар 1',
            'slug': 'krutoi-tovar-1-krutoi-brend-1',
            'brand': 'Крутой бренд',
            'photo': self.product1.photo.url,
            'price': '200.00',
            'absolute_url': '/product/krutoi-tovar-1-krutoi-brend-1',
            'quantity': 3,
            'total_it_price': '600.00',
            'total_price': '1200.00',
            'remove_cart_url': '/cart/remove/1',
            'cart_was_empty': False,
            'message': 'Товар успешно добавлен в корзину',
        }
        self.assertEqual(data, expected_data)

    def test_cart_remove_view(self):
        response = self.client.post(reverse('remove_cart', kwargs={'pk': self.product2.pk}))
        session = self.client.session
        self.assertEqual(session.get(settings.CART_SESSION_ID), {'1': {'quantity': 2, 'price': '200.00'}})

        data = json.loads(response.content)
        expected_data = {
            'slug': self.product2.slug,
            'total_price': '400.00',
            'cart_is_empty': False,
            'message': 'Товар убран из корзины',
        }
        self.assertEqual(data, expected_data)
