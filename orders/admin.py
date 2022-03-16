from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'first_name', 'last_name', 'phone',
                    'city', 'paid', 'created_at', 'updated_at']
    list_filter = ['paid', 'updated_at', 'updated_at']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
