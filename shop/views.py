import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from mptt.querysets import TreeQuerySet

from shop.forms import AddCommentForm
from shop.models import Comment, CommentDislike, CommentLike
from .models import Product, Category, Brand
from cart.forms import CartAddProductForm
from .tasks import send_notification_mail
from .templatetags.comments_tags import calc_date


def index(request):
    return render(request, 'shop/index.html')


class ViewProduct(DetailView):
    model = Product
    context_object_name = 'product'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['add_form'] = AddCommentForm()

        if self.request.user.is_authenticated:
            query_for_liked_comments = f"""
                SELECT comment_id as id
                FROM shop_commentlike
                JOIN
                (SELECT commentlike_id
                FROM shop_commentlike_users
                WHERE account_id = {self.request.user.id})
                ON(id=commentlike_id)"""

            query_for_disliked_comments = f"""
                SELECT comment_id as id
                FROM shop_commentdislike
                JOIN
                (SELECT commentdislike_id
                FROM shop_commentdislike_users
                WHERE account_id = {self.request.user.id})
                ON(id=commentdislike_id)"""

            context['liked'] = [comment.id for comment in Comment.objects.raw(query_for_liked_comments)]
            context['disliked'] = [comment.id for comment in Comment.objects.raw(query_for_disliked_comments)]

        query_for_root = f"""
            SELECT id, lft, rght, rating FROM shop_comment
            JOIN
            (SELECT id, likes - dislikes as rating
            FROM

            (SELECT id, IFNULL(likes, 0) as likes
            FROM shop_comment
            LEFT JOIN
            (SELECT shop_comment.id as id, COUNT() as likes FROM shop_comment
            JOIN shop_commentlike ON shop_commentlike.comment_id = shop_comment.id
            JOIN shop_commentlike_users ON shop_commentlike.id = shop_commentlike_users.commentlike_id
            GROUP BY shop_comment.id)
            USING(id))

            LEFT JOIN

            (SELECT id, IFNULL(dislikes, 0) as dislikes
            FROM shop_comment
            LEFT JOIN
            (SELECT shop_comment.id as id, COUNT() as dislikes FROM shop_comment
            JOIN shop_commentdislike ON shop_commentdislike.comment_id = shop_comment.id
            JOIN shop_commentdislike_users ON shop_commentdislike.id = shop_commentdislike_users.commentdislike_id
            GROUP BY shop_comment.id)
            USING(id))

            USING(id))

            USING(id)
            WHERE level = 0 and product_id = {context['product'].id}
            ORDER BY tree_id ASC, lft ASC, id ASC"""

        query_for_all = f"""
                    SELECT id, rating FROM shop_comment
                    JOIN
                    (SELECT id, likes - dislikes as rating
                    FROM

                    (SELECT id, IFNULL(likes, 0) as likes
                    FROM shop_comment
                    LEFT JOIN
                    (SELECT shop_comment.id as id, COUNT() as likes FROM shop_comment
                    JOIN shop_commentlike ON shop_commentlike.comment_id = shop_comment.id
                    JOIN shop_commentlike_users ON shop_commentlike.id = shop_commentlike_users.commentlike_id
                    GROUP BY shop_comment.id)
                    USING(id))

                    LEFT JOIN

                    (SELECT id, IFNULL(dislikes, 0) as dislikes
                    FROM shop_comment
                    LEFT JOIN
                    (SELECT shop_comment.id as id, COUNT() as dislikes FROM shop_comment
                    JOIN shop_commentdislike ON shop_commentdislike.comment_id = shop_comment.id
                    JOIN shop_commentdislike_users ON shop_commentdislike.id = shop_commentdislike_users.commentdislike_id
                    GROUP BY shop_comment.id)
                    USING(id))

                    USING(id))

                    USING(id)
                    WHERE product_id = {context['product'].id}
                    ORDER BY tree_id ASC, lft ASC, id ASC"""

        all_comments = Comment.objects.raw(query_for_all)
        root_comments = Comment.objects.raw(query_for_root)

        nodes = [node.get_descendants(include_self=True).select_related('user').select_related('comment_like')
                     .select_related('comment_dislike') for node in root_comments]

        index = 0
        for comment_tree in nodes:
            for comment in comment_tree:
                comment.rating = all_comments[index].rating
                index += 1

        paginator = Paginator(nodes, 6)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        return context


class ProductsByCategory(DetailView):
    model = Category
    template_name = 'shop/catalog_category.html'
    context_object_name = 'category'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['ancestors_tree'] = context['category'].get_ancestors(include_self=True)
        context['products'] = context['category'].get_products()

        if 'brands' in self.request.GET:
            brands = self.request.GET['brands'].split(',')
            context['choosen_brands'] = Brand.objects.filter(slug__in=brands)
            context['products'] = context['products'].filter(brand__slug__in=brands)

        paginator = Paginator(context['products'], 6)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        return context


class ProductsCatalog(ListView):
    template_name = 'shop/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.select_related('brand').all()
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(level__in=[0, 1])
        context['brands'] = Brand.objects.all()

        if 'brands' in self.request.GET:
            brands = self.request.GET['brands'].split(',')
            context['choosen_brands'] = Brand.objects.filter(slug__in=brands)
            context['products'] = context['products'].filter(brand__slug__in=brands)

        if 'search' in self.request.GET:
            search = self.request.GET['search']
            context['products'] = context['products'].filter(
                Q(title__iregex=search) | Q(category__title__iregex=search) | Q(brand__title__iregex=search))

        paginator = Paginator(context['products'], 6)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        return context


def get_brands(request):
    return render(request, 'shop/brands.html')


class AddComment(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'message': 'Need authentication'})
        data = request.POST if request.POST.get('content') else json.loads(request.body.decode("utf-8"))

        product = Product.objects.get(id=data['product_id'])
        content = data['content']
        parent_id = data.get('parent_id')
        parent = Comment.objects.get(id=parent_id) if parent_id else None
        parent_is_leaf_node = parent.is_leaf_node() if parent else None

        comment = Comment.objects.create(user=user, product=product, content=content, parent=parent)
        comment_is_root_node = comment.is_root_node()

        if parent_id:
            parent_comment = Comment.objects.select_related('user').get(id=parent_id)
            receiver = Comment.objects.get(id=parent_id).user

            send_notification_mail.delay(
                user_mail=receiver.email,
                user_comment_text=str(parent_comment),
                user_comment_date=parent_comment.created_at.strftime("%H:%M - %d %B %Y"),
                sender_username=user.username,
                product_title=product.title,
                url=request.build_absolute_uri(reverse('product', kwargs={'slug': product.slug}))
            )

        return JsonResponse({
            'id': comment.id,
            'content': content,
            'username': user.username,
            'calculated_date': calc_date(comment.created_at),
            'parent_id': parent_id,
            'parent_was_leaf_node': parent_is_leaf_node,
            'comment_is_root_node': comment_is_root_node,
            'rating': comment.count_rating(),
            'message': 'Отзыв успешно отправлен',
        })


class ToggleCommentVote(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'message': 'Need authentication'})

        data = request.POST if request.POST.get('comment_id') else json.loads(request.body.decode("utf-8"))
        comment_id = data['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)
        opinion = data['opinion']

        try:
            comment.comment_like
        except Comment.comment_like.RelatedObjectDoesNotExist as identifier:
            CommentLike.objects.create(comment=comment)

        try:
            comment.comment_dislike
        except Comment.comment_dislike.RelatedObjectDoesNotExist as identifier:
            CommentDislike.objects.create(comment=comment)

        if opinion == 'like':
            if request.user in comment.comment_like.users.all():
                comment.comment_like.users.remove(request.user)
            else:
                comment.comment_like.users.add(request.user)
                comment.comment_dislike.users.remove(request.user)
        elif opinion == 'dislike':
            if request.user in comment.comment_dislike.users.all():
                comment.comment_dislike.users.remove(request.user)
            else:
                comment.comment_dislike.users.add(request.user)
                comment.comment_like.users.remove(request.user)

        return JsonResponse({
            'rating': comment.count_rating(),
        })
