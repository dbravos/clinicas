from .models import Usuarios

def clinica_actual(request):

    nombre_clinica = request.session.get('clinica_actual', 'DEMO')
    lista_usuarios = []
    if nombre_clinica:
        lista_usuarios = Usuarios.objects.filter(clinica=nombre_clinica).order_by('nombre')
    return {
        'clinica_actual': nombre_clinica,
        'clinica_nombre': request.session.get('clinica_nombre', ''),
        'usuario_autenticado': request.session.get('usuario_autenticado', False),
        'usuario_id': request.session.get('usuario_id'),
        'usuario_no': request.session.get('usuario_no'),
        'usuario_nombre': request.session.get('usuario_nombre', ''),
        'usuario_cargo': request.session.get('usuario_cargo', ''),
        'usuario_permisos': request.session.get('usuario_permisos', ''),
        'usuarios_para_login':lista_usuarios
    }