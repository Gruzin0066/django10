from django import template
from blog.models import Category, PostTags

register = template.Library()


@register.simple_tag()
def get_category():
    return Category.objects.all()

@register.simple_tag()
def get_tags():
    return PostTags.objects.all()