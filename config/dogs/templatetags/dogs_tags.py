from django import template
from ..models import Category, Photo

register = template.Library()


@register.simple_tag
def total_photos():
    return Photo.objects.count()


@register.inclusion_tag('dogs/category_menu.html')
def category_menu():
    categories = Category.objects.all()
    return {'categories': categories}