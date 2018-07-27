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
def in_dict_str2(a_dict,cc):
    value = int(cc.split('_')[-1])
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

@register.filter
def contains2(a_str,value):
    if a_str:
        value = int(value.split('_')[-1])
        if a_str.startswith('Au'):
            a_str = '0'
        else:
            a_str = '1'
        if value == int(a_str):
            return True
    return False