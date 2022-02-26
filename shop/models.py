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
        products = Product.objects.filter(category__in=categories)
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
        return reverse('brand', kwargs={"slug": self.slug})

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
