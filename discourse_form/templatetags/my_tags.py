from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    if num == 0:
        return 1
    return num % val

@register.filter
def novacio(num):
    if num == "":
        return False
    return True

@register.filter
def in_dict(a_dict,skill):
    if skill in a_dict:
        return a_dict[skill]
    return []