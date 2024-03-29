from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


# class FileInline(admin.TabularInline):
#     model = File

# @admin.register(FileGroup)
# class FileGroupAdmin(admin.ModelAdmin):
#     inlines = [
#         FileInline,
#     ]


admin.site.register(LayerGroup)
admin.site.register(Image)
admin.site.register(Celery)
admin.site.register(UsersCollection)