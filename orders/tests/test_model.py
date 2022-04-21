import tempfile

from django.test import TestCase
from slugify import slugify

from account.models import Account
from orders.models import Order, OrderItem
from shop.models import Brand, Category, Product


class OrderModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(title='Крутой бренд', slug=slugify('Крутой бренд'))
        self.category = Category.objects.create(title='Крутая категория', slug=slugify('krutaia-kategoriia'))
        self.product = Product.objects.create(title='Крутой товар', slug='krutoi-tovar', category=self.category,
                                              brand=self.brand, photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                              price=300, stock=30)
        self.user = Account.objects.create(email="user@mail.com", username="user", password="12345")
        self.order = Order.objects.create(customer=self.user, first_name="first_name", last_name="last_name",
                                          patronymic="patronymic", phone="+380999999999", city="city",
                                          address="address", postal_code="99999", paid=True)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product,
                                                   price=self.product.price, quantity=2)

    def test_order_str_method(self):
        self.assertEqual(str(self.order), 'Заказ 1')

    def test_order_get_total_cost(self):
        self.assertEqual(self.order.get_total_cost(), 600.00)

    def test_order_item_str_method(self):
        self.assertEqual(str(self.order_item), "Заказ 1 - 1: Крутой товар")

    def test_order_item_get_cost(self):
        self.assertEqual(self.order_item.get_cost(), 600.00)
