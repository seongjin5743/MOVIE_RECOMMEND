# movies/templatetags/my_filters.py
from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None

@register.filter
def contains(value, arg):
    if value:
        return arg in value
    return False