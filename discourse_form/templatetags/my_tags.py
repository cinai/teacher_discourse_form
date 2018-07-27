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

@register.filter
def in_dict_str(a_dict,cc):
    value = int(cc.split('_')[-1])+1
    if value in a_dict:
        return a_dict[value]
    return []

@register.filter
def contains(a_list,value):
    if a_list:
        value = int(value.split('_')[-1])
        if value+1 in a_list:
            return True
    return False