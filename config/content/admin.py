from django.contrib import admin
from .models import Section, Content, Question


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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'is_answered', 'created_at')
    list_filter = ('is_answered', 'created_at')
    search_fields = ('text', 'answer', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
