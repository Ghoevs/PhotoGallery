from django.contrib import admin
from .models import Breed, Dog, Pedigree, Review


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'owner', 'is_active', 'views', 'created_at')
    list_filter = ('breed', 'is_active', 'age')
    search_fields = ('name', 'description')
    readonly_fields = ('views', 'created_at')
    list_editable = ('is_active',)


@admin.register(Pedigree)
class PedigreeAdmin(admin.ModelAdmin):
    list_display = ('dog', 'father', 'mother', 'created_at')
    search_fields = ('dog__name', 'father', 'mother')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('dog', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('dog__name', 'user__username', 'text')
