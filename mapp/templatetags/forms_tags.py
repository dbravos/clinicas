

# forms_tags.py
from django import template

register = template.Library()

@register.simple_tag
def get_form_field(form, field_name):
    try:
        field = form[field_name]
        field.field.widget.attrs.update({'class': 'form-check-input'})  # Asegura clases
        return field
    except KeyError:
        return None
@register.filter
def get_field(form, field_name):
    """Obtiene un campo del formulario por su nombre"""
    return form[field_name]
# tu_app/templatetags/form_tags.py (añadir esto)
@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)

@register.filter
def splitealo(value, delimiter=","):
    return int(value.split(delimiter))




@register.filter(name='attr')  # Registra el filtro 'attr'
def attr(field, css):
    """
    Añade atributos HTML a un campo de formulario.
    Uso: {{ field|attr:"class:form-control,placeholder:Ingrese texto" }}
    """
    attrs = {}
    for pair in css.split(','):
        key, value = pair.split(':')
        attrs[key] = value
    return field.as_widget(attrs=attrs)

@register.filter
def add_class(field, css_class):
    """Añade una clase CSS a un campo de formulario"""
    return field.as_widget(attrs={"class": css_class})
