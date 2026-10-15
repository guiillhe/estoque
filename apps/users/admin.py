from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'enterprise', 'is_admin', 'is_buyer', 'is_supplier']
    list_filter = ['enterprise', 'is_admin', 'is_buyer', 'is_supplier']
    search_fields = ['username', 'first_name', 'email']



admin.site.register(User, UserAdmin)
