from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'is_active', 'is_superuser', 'created_at')
    list_display_links = ('pk', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('role', 'is_superuser', 'is_active')
    save_as = True
