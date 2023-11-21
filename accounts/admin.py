from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin (UserAdmin):
    ordering = ['date_joined']
    list_display = [
        'email', 'first_name', 'last_name', 'is_active',
        'email_verified', 'is_staff']
    readonly_fields = ['date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

