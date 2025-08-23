from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from users.models import User


# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'get_html_photo')
    list_display_links = ('username', 'email', 'phone')

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')
        return None

    get_html_photo.short_description = 'Фото'

    # Расширяем fieldsets чтобы добавить кастомные поля в админку
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email',
                'phone', 'date_birth', 'address', 'photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Verification'), {
            'fields': ('verification_token', 'token_created_at'),
            'classes': ('collapse',)  # Сворачиваемый раздел
        }),
    )

    # Поля при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone', 'password1', 'password2',
                'first_name', 'last_name', 'date_birth', 'address'
            ),
        }),
    )

    ordering = ('username',)



admin.site.register(User, UserAdmin)