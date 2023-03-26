from django import template

register = template.Library()

@register.filter

def custom_truncatechars(value, arg):
    if len(value) <= arg:
        return value
    else:
        return value[:arg] + "・・・"
