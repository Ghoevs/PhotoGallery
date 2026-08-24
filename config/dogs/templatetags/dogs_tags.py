from django import template
from ..models import Breed

register = template.Library()


@register.simple_tag
def total_dogs():
    from ..models import Dog
    return Dog.objects.count()


@register.inclusion_tag('dogs/breed_menu.html')
def breed_menu():
    breeds = Breed.objects.all()
    return {'breeds': breeds}
