import tempfile

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from slugify import slugify

from account.models import Account
from orders.models import Order, OrderItem
from shop.models import Brand, Category, Product


class OrderModelTest(TestCase):

    def setUp(self):
        brand = Brand.objects.create(title='Крутой бренд', slug=slugify('Крутой бренд'))
        category = Category.objects.create(title='Крутая категория', slug=slugify('krutaia-kategoriia'))
        self.product = Product.objects.create(title='Крутой товар', slug='krutoi-tovar', category=category,
                                              brand=brand, photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                              price=300, stock=30)
        self.user = Account.objects.create(email="user@mail.com", username="user", password="12345")
        self.user.set_password('12345')
        self.user.save()

    def test_order_create_if_not_logged(self):
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 403)

    def test_order_create_access(self):
        self.client.login(username="user", password="12345")
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order.html')

    def test_order_create_invalid(self):
        self.client.login(username="user", password="12345")

        response = self.client.post(reverse('order_create'), data={
            'first_name': "",
            'last_name': "",
            'patronymic': "",
            'phone': "",
            'city': "",
            'address': "",
            'postal_code': "",
            'paid': False,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Order.objects.all()), 0)

    def test_order_create_valid(self):
        self.client.login(username="user", password="12345")
        session = self.client.session

        session.update({
            settings.CART_SESSION_ID: {
                '1': {
                    'quantity': 2,
                    'price': '300.00'
                }
            },
        })
        session.save()

        response = self.client.post(reverse('order_create'), data={
            'first_name': "first_name",
            'last_name': "last_name",
            'patronymic': "patronymic",
            'phone': "+380999999999",
            'city': "city",
            'address': "address",
            'postal_code': "99999",
            'paid': True,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('orders/created.html')
        order_items = Order.objects.get(pk=1).items.all()
        self.assertQuerysetEqual(order_items, OrderItem.objects.all())
