from django.test import TestCase
from slugify import slugify
import tempfile

from shop.models import Product, Category, Brand


class ShopModelTest(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(title='Крутой бренд', slug=slugify('Крутой бренд'))
        self.root_category = Category.objects.create(title='parent категория', slug=slugify('root-kategoriia'))
        self.child_category = Category.objects.create(title='child категория', slug=slugify('child-kategoriia'),
                                                      parent=self.root_category)
        self.product = Product.objects.create(title='Крутой товар', slug='krutoi-tovar', category=self.child_category,
                                              brand=self.brand, photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                              price=300, stock=30)

    def test_brand_get_absolute_url(self):
        self.assertEqual(self.brand.get_absolute_url(), '/brand/krutoi-brend')

    def test_category_root_slug_creation(self):
        self.assertEqual(self.root_category.slug, 'root-kategoriia')

    def test_category_child_slug_creation(self):
        self.assertEqual(self.child_category.slug, 'root-kategoriia-child-kategoriia')

    def test_category_get_absolute_url(self):
        self.assertEqual(self.child_category.get_absolute_url(), '/catalog/root-kategoriia-child-kategoriia')

    def test_category_get_products(self):
        self.assertNotEqual(self.product.category, self.root_category)
        self.assertIn(self.product, self.root_category.get_products())

    def test_product_slug_creation(self):
        self.assertEqual(self.product.slug, 'krutoi-tovar-krutoi-brend-1')

    def test_product_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), '/product/krutoi-tovar-krutoi-brend-1')
