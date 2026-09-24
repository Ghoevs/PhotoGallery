from django.contrib import admin
from .models import Category, Photo, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'is_active', 'views', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('views', 'created_at')
    list_editable = ('is_active',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('photo__title', 'user__username', 'text')