from django import template

register = template.Library()


# --- 1. Filtros para dividir textos (necesario para los tabs) ---

@register.filter(name='split')
def split(value, key):
    """Divide un string por un separador. Uso: '1,2,3'|split:','"""
    return value.split(key)


@register.filter
def split_pairs(value):
    """
    Convierte '3:Deseo,4:Problemas' en una lista pareada.
    Necesario para el bucle de las preguntas 3 a 7.
    """
    if not value:
        return []
    items = value.split(',')
    # Devuelve una lista de listas: [['3', 'Deseo'], ['4', 'Problemas']]
    return [item.split(':') for item in items]


# --- 2. Filtros de lógica visual ---

@register.filter
def slugify_assist(value):
    """Mapea el número de pregunta con el ID del div HTML"""
    mapping = {
        '3': 'deseo',
        '4': 'problemas',
        '5': 'dejado',
        '6': 'preocupacion',
        '7': 'reducir'
    }
    return mapping.get(str(value), str(value))


@register.filter
def nivel_riesgo(puntos):
    """Calcula el nivel de riesgo basado en los puntos (para los badges)"""
    try:
        val = int(puntos)
    except (ValueError, TypeError):
        return "Bajo"

    if val <= 3:
        return "Bajo"
    elif val <= 26:
        return "Medio"
    else:
        return "Alto"


# --- 3. Tags para obtener campos del formulario dinámicamente ---

@register.simple_tag
def get_form_field(form, field_name):
    """Obtiene un campo por su nombre string: form['p1s1']"""
    try:
        return form[field_name]
    except KeyError:
        return None


@register.simple_tag
def get_otras_field(form, p_num):
    """
    ESTA ES LA QUE TE FALTABA.
    Obtiene el campo 'asistotras' correcto según el número de pregunta.
    """
    if str(p_num) == '1':
        name = 'asistotras'
    else:
        name = f'asistotras{p_num}'

    try:
        return form[name]
    except KeyError:
        return None