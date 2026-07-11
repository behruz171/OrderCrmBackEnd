from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'client_phone', 'status', 'user', 'created_at']
    list_filter = ['status', 'user']
    search_fields = ['client_name', 'client_phone']
    inlines = [OrderItemInline]
