from django.contrib.auth import get_user_model
from django.test import TestCase
from slugify import slugify
import tempfile

from shop.models import Product, Category, Brand, Comment, CommentLike, CommentDislike


class ShopModelTest(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(title='Крутой бренд', slug=slugify('Крутой бренд'))
        self.root_category = Category.objects.create(title='parent категория', slug=slugify('root-kategoriia'))
        self.child_category = Category.objects.create(title='child категория', slug=slugify('child-kategoriia'),
                                                      parent=self.root_category)
        self.product = Product.objects.create(title='Крутой товар', slug='krutoi-tovar', category=self.child_category,
                                              brand=self.brand, photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                              price=300, stock=30)
        self.user1 = get_user_model().objects.create(email='user1@mail.com', username='user1', password='12345')
        self.user2 = get_user_model().objects.create(email='user2@mail.com', username='user2', password='12345')
        self.comment = Comment.objects.create(content="Comment content", user=self.user1, product=self.product)

    def test_brand_get_absolute_url(self):
        self.assertEqual(self.brand.get_absolute_url(), '/brand/krutoi-brend')

    def test_category_str_method(self):
        self.assertEqual(str(self.child_category), 'child категория')

    def test_category_root_slug_creation(self):
        self.assertEqual(self.root_category.slug, 'root-kategoriia')

    def test_category_child_slug_creation(self):
        self.assertEqual(self.child_category.slug, 'root-kategoriia-child-kategoriia')

    def test_category_get_absolute_url(self):
        self.assertEqual(self.child_category.get_absolute_url(), '/catalog/root-kategoriia-child-kategoriia')

    def test_category_get_products(self):
        self.assertNotEqual(self.product.category, self.root_category)
        self.assertIn(self.product, self.root_category.get_products())

    def test_product_str_method(self):
        self.assertEqual(str(self.product), 'Крутой товар')

    def test_product_slug_creation(self):
        self.assertEqual(self.product.slug, 'krutoi-tovar-krutoi-brend-1')

    def test_product_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), '/product/krutoi-tovar-krutoi-brend-1')

    def test_comment_model_count_rating(self):
        self.assertEqual(self.comment.count_rating(), 0)

    def test_comment_like(self):
        comment_like = CommentLike.objects.create(comment=self.comment)
        self.assertEqual(str(comment_like), 'Like for comment 1: user1 - Comment cont...')
        comment_like.users.add(self.user1)
        comment_like.users.add(self.user2)
        self.assertEqual(self.comment.count_rating(), 2)

    def test_comment_dislike(self):
        comment_dislike = CommentDislike.objects.create(comment=self.comment)
        self.assertEqual(str(comment_dislike), 'Dislike for comment 1: user1 - Comment cont...')
        comment_dislike.users.add(self.user1)
        comment_dislike.users.add(self.user2)
        self.assertEqual(self.comment.count_rating(), -2)
