def clinica_actual(request):
    return {
        'clinica_actual': request.session.get('clinica_actual', 'Demostracion'),
        'clinica_nombre': request.session.get('clinica_nombre', ''),
        'usuario_autenticado': request.session.get('usuario_autenticado', False),
        'usuario_id': request.session.get('usuario_id'),
        'usuario_no': request.session.get('usuario_no'),
        'usuario_nombre': request.session.get('usuario_nombre', ''),
        'usuario_cargo': request.session.get('usuario_cargo', ''),
        'usuario_permisos': request.session.get('usuario_permisos', '')
    }