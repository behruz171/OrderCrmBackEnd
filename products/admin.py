from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name']
    list_filter = ['user']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'dimensions', 'price', 'user', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['user', 'category']
