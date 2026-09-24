from django.contrib import admin
from .models import Section, Content


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'author', 'views', 'is_published', 'created_at')
    list_filter = ('section', 'is_published')
    search_fields = ('title', 'body')
    readonly_fields = ('views', 'created_at', 'updated_at')