from django.test import TestCase
from django.urls import reverse
from slugify import slugify
import tempfile

from shop.models import Product, Category, Brand


class ShopViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        brand1 = Brand.objects.create(title='Крутой бренд 1', slug=slugify('Крутой бренд 1'))
        brand2 = Brand.objects.create(title='Крутой бренд 2', slug=slugify('Крутой бренд 2'))
        parent_category = Category.objects.create(title='parent категория', slug=slugify('root-kategoriia'))
        child_category = Category.objects.create(title='child категория', slug=slugify('child-kategoriia'),
                                                 parent=parent_category)
        for num in range(1, 11):
            Product.objects.create(title=f'Крутой товар {num}', slug=f'krutoi-tovar {num}', category=child_category,
                                   brand=brand1, photo=tempfile.NamedTemporaryFile(suffix=".jpg").name, price=300,
                                   stock=30)

    def test_index_access(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_product_view_access(self):
        product = Product.objects.get(pk=2)
        response = self.client.get(reverse('product', kwargs={'slug': product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')

    def test_catalog_category_access(self):
        category = Category.objects.get(pk=2)
        response = self.client.get(reverse('category', kwargs={'slug': category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/catalog_category.html')

    def test_brands_access(self):
        response = self.client.get(reverse('brands'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/list_brands.html')

    def test_catalog_pagination(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['page_obj'].has_other_pages)
        self.assertTrue(len(response.context['page_obj']) == 6)

    def test_catalog_brands(self):
        response = self.client.get('/catalog?brands=krutoi-brend-1,krutoi-brend-2')
        self.assertEqual(response.status_code, 200)
        brands = Brand.objects.filter(slug__in=response.context['request'].GET['brands'].split(','))
        self.assertQuerysetEqual(response.context['choosen_brands'], brands)

    def test_catalog_search(self):
        response = self.client.get('/catalog?search=крутой')
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(len(products), len(products.filter(title__iregex='крутой')))

    def test_catalog_category_pagination(self):
        category = Category.objects.get(pk=2)
        response = self.client.get(reverse('category', kwargs={'slug': category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['page_obj'].has_other_pages)
        self.assertTrue(len(response.context['page_obj']) == 6)

    def test_catalog_category_brands(self):
        response = self.client.get('/catalog/root-kategoriia?brands=krutoi-brend-1,krutoi-brend-2')
        self.assertEqual(response.status_code, 200)
        brands = Brand.objects.filter(slug__in=response.context['request'].GET['brands'].split(','))
        self.assertQuerysetEqual(response.context['choosen_brands'], brands)

    def test_brands_inclusion_tag(self):
        response = self.client.get(reverse('brands'))
        self.assertEqual(response.status_code, 200)
        brand1 = Brand.objects.get(pk=1)
        brand2 = Brand.objects.get(pk=2)
        self.assertEqual(response.context['lists_brands'], [[brand1], [brand2], [], []])
