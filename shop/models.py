from django.conf import settings
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify


class Category(MPTTModel):
    title = models.CharField(max_length=50, verbose_name="Название")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=60, unique=True, verbose_name="url", null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    def get_products(self):
        """Return all self and descendants products"""
        categories = self.get_descendants(include_self=True)
        products = Product.objects.select_related('brand').filter(category__in=categories)
        return products

    def save(self, **kwargs):
        super(Category, self).save()
        if not self.is_root_node():
            root = self.get_root()
            if not self.slug.startswith(root.slug):
                self.slug = root.slug + '-' + slugify(self.title)
                super(Category, self).save()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['-title']


class Brand(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=30, unique=True, verbose_name="url")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog') + "?brands=" + self.slug

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=111, verbose_name="url", unique=True)
    photo = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name="Фото")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="Количество")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")
    category = TreeForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Бренд')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def save(self, **kwargs):
        super(Product, self).save()
        if not self.slug.endswith(self.brand.slug + '-' + str(self.pk)):
            self.slug += '-' + self.brand.slug + '-' + str(self.id)
            super(Product, self).save()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = models.TextField(verbose_name="Содержимое")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    is_public = models.BooleanField(verbose_name="Публичный", default=True)
    is_removed = models.BooleanField(verbose_name="Удален", default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.content[:12]}{'...' if len(self.content) > 12 else ''}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    class MPTTMeta:
        order_insertion_by = ('-created_at', )

    def count_rating(self):
        """
        Returns number of likes minus dislikes
        """
        likes = 0
        dislikes = 0

        try:
            likes = self.comment_like.users.count()
        except Comment.comment_like.RelatedObjectDoesNotExist as identifier:
            CommentLike.objects.create(comment=self)

        try:
            dislikes = self.comment_dislike.users.count()
        except Comment.comment_dislike.RelatedObjectDoesNotExist as identifier:
            CommentDislike.objects.create(comment=self)

        return likes - dislikes


class CommentLike(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='comment_like')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Like for comment {self.comment.id}: {str(self.comment)}"

    class Meta:
        verbose_name = 'Лайки к комментарию'
        verbose_name_plural = 'Лайки к комментариям'


class CommentDislike(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='comment_dislike')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dislike for comment {self.comment.id}: {str(self.comment)}"

    class Meta:
        verbose_name = 'Дизлайки к комментарию'
        verbose_name_plural = 'Дизлайки к комментариям'
