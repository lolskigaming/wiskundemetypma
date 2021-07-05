from random import randint
from django import template

register = template.Library()

@register.simple_tag
def random(x, y):
    return randint(x, y)