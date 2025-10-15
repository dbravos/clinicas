from django import template

register = template.Library()

@register.filter(name='nivel_riesgo')
def nivel_riesgo(puntos):
    """Filtro de plantilla que convierte un puntaje en un nivel de riesgo."""
    try:

        puntos = int(puntos) # Asegurarse de que es un número
    except (ValueError, TypeError):
        return "" # O devuelve un valor por defecto

    if puntos <= 3:
        return "Bajo"
    elif puntos <= 26:
        return "Medio"
    else:
        return "Alto"