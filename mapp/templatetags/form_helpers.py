# En tu_app/templatetags/form_helpers.py
from django import template

register = template.Library()

@register.inclusion_tag('includes/radio_field.html')
def render_radio_field(field, col_class='col-2'):
    return {'field': field, 'col_class': col_class}