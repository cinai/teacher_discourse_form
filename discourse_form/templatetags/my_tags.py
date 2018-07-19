from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    if num == 0:
        return 1
    return num % val