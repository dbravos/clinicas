from django import template

register = template.Library()

@register.filter
def to(value, arg):
    return range(int(value), int(arg) + 1)

@register.filter
def getattr(obj, attr_name):
    """Versión segura que evita recursión"""
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None

@register.filter(name='times')
def times(number):
    """Genera un rango de números hasta el valor especificado."""
    return range(1, 26)