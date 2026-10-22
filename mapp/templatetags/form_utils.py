from django import template

register = template.Library()

@register.filter
def get_field_value(form, field_pattern):
    field_name = field_pattern % {'field': 'papa'}  # Ejemplo de patrón
    return form[field_name]