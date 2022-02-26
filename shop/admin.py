from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Brand, Product

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
    prepopulated_fields={"slug": ('title',)}
)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'brand', 'is_available', 'created_at', 'updated_at', 'get_photo')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title',)
    list_filter = ('is_available', 'category', 'brand')
    fields = ('title', 'slug', 'description', 'category', 'brand', 'price', 'stock', 'photo',
              'get_photo', 'is_available', 'created_at', 'updated_at')
    readonly_fields = ('get_photo', 'created_at', 'updated_at')
    save_on_top = True
    prepopulated_fields = {"slug": ("title",)}

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'Миниатюра'


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
