from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subscription


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone', 'role', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    search_fields = ('email', 'username', 'phone', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio', 'birth_date')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')
        }),
        ('Важные даты', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'started_at', 'expires_at')
    list_filter = ('is_active', 'plan')
    search_fields = ('user__username', 'user__email')
    list_editable = ('is_active', 'plan')
    readonly_fields = ('created_at',)