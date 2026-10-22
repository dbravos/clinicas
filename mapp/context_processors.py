from .models import Usuarios

# Sección del expediente a la que pertenece cada pantalla (para resaltar la navegación).
SECCIONES_EXPEDIENTE = {
    'evaluaciones': ['einicial', 'assist', 'psicosis', 'sdevida', 'usodrogas', 'ansiedad',
                     'depresion', 'marcadores', 'riesgos'],
    'consejeria': ['razones', 'valorizacion', 'planConsejeria', 'listaSesiones', 'capturaSesion',
                   'capturaSesion_con_id', 'escanear_tarea', 'lista_tareas_escaneadas',
                   'listaSesionesGrupales', 'capturaSesionGrupal', 'capturaSesionGrupal_con_id'],
    'psicologia': ['hojaAtencionPs', 'listaSesionesPS', 'capturaSesionPS', 'capturaSesionPS_con_id'],
    'medico': ['medicoInicial', 'emisionDerecetas', 'historiaClinica'],
    'seguimiento': ['seguimiento', 'listaSesionesS', 'capturaSesionS', 'capturaSesionS_con_id'],
}
SECCION_POR_VISTA = {vista: seccion for seccion, vistas in SECCIONES_EXPEDIENTE.items() for vista in vistas}

def clinica_actual(request):
    match = getattr(request, 'resolver_match', None)
    url_name = match.url_name if match else ''

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
        'usuarios_para_login':lista_usuarios,
        'seccion_expediente': SECCION_POR_VISTA.get(url_name, ''),
        # Altas, salidas, documentos y reporte de internos: solo administración y oficina
        'puede_gestionar_internos': any(r in (request.session.get('usuario_permisos') or '').upper()
                                        for r in ('ADMIN', 'OFICINA')),
    }