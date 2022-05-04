import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from slugify import slugify
import tempfile

from shop.models import Product, Category, Brand, Comment, CommentDislike, CommentLike


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

        user1 = get_user_model().objects.create(email='user1@mail.com', username='user1', password='12345')
        user1.set_password('12345')
        user1.save()
        user2 = get_user_model().objects.create(email='user2@mail.com', username='user2', password='12345')
        user2.set_password('12345')
        user2.save()
        comment = Comment.objects.create(content="Comment content", user=user1, product=Product.objects.get(pk=1))

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

    def test_add_comment_not_authenticated(self):
        response = self.client.post(reverse('add_comment'), {
            'content': 'Comment content 2',
            'product_id': 1,
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'message': 'Need authentication',
        }
        self.assertEqual(data, expected_data)

    def test_add_comment(self):
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('add_comment'), {
            'content': 'Comment content 2',
            'product_id': 1,
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'id': 2,
            'content': 'Comment content 2',
            'username': 'user1',
            'calculated_date': 'Less than minute ago',
            'parent_id': None,
            'parent_was_leaf_node': None,
            'comment_is_root_node': True,
            'rating': 0,
            'message': 'Отзыв успешно отправлен',
        }
        self.assertEqual(data, expected_data)

    def test_toggle_comment_vote_not_authenticated(self):
        response = self.client.post(reverse('toggle_comment_vote'), {
            'comment_id': 1,
            'opinion': 'like',
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'message': 'Need authentication',
        }
        self.assertEqual(data, expected_data)

    def test_toggle_comment_vote_like(self):
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('toggle_comment_vote'), {
            'comment_id': 1,
            'opinion': 'like',
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'rating': 1,
        }
        self.assertEqual(data, expected_data)
        comment = Comment.objects.get(pk=1)
        self.assertEqual(comment.count_rating(), 1)

    def test_toggle_comment_vote_like_with_like_before(self):
        comment = Comment.objects.get(pk=1)
        comment_like = CommentLike.objects.create(comment=comment)
        comment_like.users.add(get_user_model().objects.get(pk=1))
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('toggle_comment_vote'), {
            'comment_id': 1,
            'opinion': 'like',
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'rating': 0,
        }
        self.assertEqual(data, expected_data)
        comment = Comment.objects.get(pk=1)
        self.assertEqual(comment.count_rating(), 0)

    def test_toggle_comment_vote_dislike(self):
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('toggle_comment_vote'), {
            'comment_id': 1,
            'opinion': 'dislike',
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'rating': -1,
        }
        self.assertEqual(data, expected_data)
        comment = Comment.objects.get(pk=1)
        self.assertEqual(comment.count_rating(), -1)

    def test_toggle_comment_vote_dislike_with_dislike_before(self):
        comment = Comment.objects.get(pk=1)
        comment_dislike = CommentDislike.objects.create(comment=comment)
        comment_dislike.users.add(get_user_model().objects.get(pk=1))
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('toggle_comment_vote'), {
            'comment_id': 1,
            'opinion': 'dislike',
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_data = {
            'rating': 0,
        }
        self.assertEqual(data, expected_data)
        comment = Comment.objects.get(pk=1)
        self.assertEqual(comment.count_rating(), 0)
