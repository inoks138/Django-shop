import tempfile

from django.test import TestCase
from slugify import slugify

from account.models import Account
from orders.forms import OrderCreateForm
from shop.models import Brand, Category, Product


class OrderFormTest(TestCase):
    @classmethod
    def setUp(cls):
        brand = Brand.objects.create(title='Крутой бренд', slug=slugify('Крутой бренд'))
        category = Category.objects.create(title='Крутая категория', slug=slugify('krutaia-kategoriia'))
        Product.objects.create(title='Крутой товар', slug='krutoi-tovar', category=category, brand=brand,
                               photo=tempfile.NamedTemporaryFile(suffix=".jpg").name, price=300, stock=30)
        user = Account.objects.create(email="user@mail.com", username="user", password="12345")
        user.set_password('12345')
        user.save()

    def test_order_create_form_invalid(self):
        form = OrderCreateForm(data={
            'customer': None,
            'first_name': "",
            'last_name': "",
            'patronymic': "",
            'phone': "",
            'city': "",
            'address': "",
            'postal_code': "",
            'paid': False,
        })
        self.assertFalse(form.is_valid())

    def test_order_create_form_valid(self):
        user = Account.objects.get(pk=1)
        form = OrderCreateForm(data={
            'customer': user,
            'first_name': "first_name",
            'last_name': "last_name",
            'patronymic': "patronymic",
            'phone': "+380999999999",
            'city': "city",
            'address': "address",
            'postal_code': "99999",
            'paid': True,
        })
        self.assertTrue(form.is_valid())
