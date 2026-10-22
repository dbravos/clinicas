from django import template

register = template.Library()


@register.filter
def obtener_atributo(obj, attr_name):
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


import builtins
@register.filter
def valor_editado(form, field_name):
    instance = form.instance

    metodo = f"get_{field_name}_display"
    if builtins.hasattr(instance, metodo):
        return getattr(instance, metodo)()

    valor = builtins.getattr(instance, field_name, None)

    if isinstance(valor, bool):
        return "Sí" if valor else "No"

    try:
        return valor.strftime("%d/%m/%Y")
    except:
        pass



    if isinstance(valor, (int, float)) and (
        "aportacion" in field_name or
        "saldo" in field_name or
        "cuota" in field_name
    ):
        return f"${valor:,.2f}"

    return valor if valor else "-"