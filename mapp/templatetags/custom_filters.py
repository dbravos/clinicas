from django import template

register = template.Library()


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
    return range(1, number + 1)

@register.filter
def get_field(form, field_name):
    return form[field_name]

@register.filter
def get_form_field(form, field_name):
    """Acceso seguro a campos de formulario"""
    try:
        return form[field_name]  # Acceso directo al campo del formulario
    except KeyError:
        return None


@register.filter
def moneda(valor):
    try:
        valor = float(valor)
        # El formato ",.2f" agrega comas de miles y 2 decimales
        return f"${valor:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"