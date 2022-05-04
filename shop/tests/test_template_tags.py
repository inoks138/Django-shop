from datetime import timedelta
from django.test import TestCase

from django.urls import reverse
from django.utils.timezone import now
from slugify import slugify

from shop.models import Brand
from shop.templatetags.comments_tags import calc_date


class ShopTemplateTagsTest(TestCase):
    def test_brands_inclusion_tag(self):
        brand1 = Brand.objects.create(title='Крутой бренд 1', slug=slugify('Крутой бренд 1'))
        brand2 = Brand.objects.create(title='Крутой бренд 2', slug=slugify('Крутой бренд 2'))
        response = self.client.get(reverse('brands'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lists_brands'], [[brand1], [brand2], [], []])

    def test_calc_date(self):
        date = now() - timedelta(seconds=3)
        self.assertEqual(calc_date(date), 'Less than minute ago')

        date = now() - timedelta(minutes=1)
        self.assertEqual(calc_date(date), '1 minute ago')
        date = now() - timedelta(minutes=4)
        self.assertEqual(calc_date(date), '4 minutes ago')

        date = now() - timedelta(hours=1)
        self.assertEqual(calc_date(date), '1 hour ago')
        date = now() - timedelta(hours=4)
        self.assertEqual(calc_date(date), '4 hours ago')

        date = now() - timedelta(days=1)
        self.assertEqual(calc_date(date), '1 day ago')
        date = now() - timedelta(days=4)
        self.assertEqual(calc_date(date), '4 days ago')

        date = now() - timedelta(days=40)
        self.assertEqual(calc_date(date), '1 month ago')
        date = now() - timedelta(days=80)
        self.assertEqual(calc_date(date), '2 months ago')

        date = now() - timedelta(days=365)
        self.assertEqual(calc_date(date), '1 year ago')
        date = now() - timedelta(days=365*3)
        self.assertEqual(calc_date(date), '3 years ago')
