# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
         'fields': ('role', 'phone', 'profile_picture', 'address')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
