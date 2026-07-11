from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('phone', 'company')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'company']
