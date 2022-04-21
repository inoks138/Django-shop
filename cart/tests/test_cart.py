import tempfile

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from slugify import slugify

from shop.models import Product, Category, Brand


class CartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        brand = Brand.objects.create(title='Крутой бренд', slug=slugify('Крутой бренд'))
        category = Category.objects.create(title='Крутая категория', slug=slugify('krutaia-kategoriia'))
        for num in range(1, 11):
            Product.objects.create(title=f'Крутой товар', slug=f'krutoi-tovar', category=category, brand=brand,
                                   photo=tempfile.NamedTemporaryFile(suffix=".jpg").name, price=300, stock=30)

        client = Client()
        response = client.get(reverse('home'))
        cls.cart = response.context['cart']

    def test_cart_add_method(self):
        products = Product.objects.all()
        for i in range(5):
            self.cart.add(products[i])
        self.assertEqual(len(self.cart), 5)
        cart_list = list(self.cart)
        for i in range(5):
            self.assertEqual(cart_list[i]['product'], products[i])

    def test_cart_add_method_update_quantity_true(self):
        self.cart.add(Product.objects.get(pk=1))
        self.cart.add(Product.objects.get(pk=1), quantity=5, update_quantity=True)
        self.assertEqual(self.cart.cart['1']['quantity'], 5)

    def test_cart_total_price(self):
        self.cart.add(Product.objects.get(pk=2), quantity=2, update_quantity=True)
        self.cart.add(Product.objects.get(pk=3), quantity=3, update_quantity=True)
        total_price = sum([product['price'] * product['quantity'] for product in list(self.cart)])
        self.assertEqual(self.cart.get_total_price(), total_price)

    def test_cart_remove_method(self):
        product = Product.objects.get(pk=4)
        self.cart.add(product)
        self.assertIn(str(product.id), self.cart.cart)
        self.cart.remove(product)
        self.assertNotIn(str(product.id), self.cart.cart)

    def test_cart_clear(self):
        self.cart.clear()
        self.assertFalse(hasattr(self.cart.session, settings.CART_SESSION_ID))
