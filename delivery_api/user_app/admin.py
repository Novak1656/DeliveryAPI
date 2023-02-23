from django.contrib import admin
from .models import User, UserAddresses


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'is_active', 'is_superuser', 'created_at')
    list_display_links = ('pk', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('role', 'is_superuser', 'is_active')
    save_as = True


@admin.register(UserAddresses)
class UserAddresses(admin.ModelAdmin):
    list_display = ('pk', 'user', 'get_address', 'order_count', 'last_order')
    list_display_links = ('pk',)
    search_fields = ('user__username',)
    list_filter = ('order_count',)
    save_as = True

    def get_address(self, instance):
        return instance.get_full_address()

    get_address.short_description = 'Адрес'
