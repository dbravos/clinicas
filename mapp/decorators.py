from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def permiso_requerido(rol_necesario):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            # 1. VERIFICAR SI LA SESIÓN SIGUE VIVA (TIMEOUT)
            # Si la variable de sesión de Django murió, pero intentan entrar:
            if not request.session.get('usuario_autenticado'):

                # A. Borramos solo datos de usuario (dejamos la clinica viva)
                keys_to_delete = [
                    'usuario_autenticado', 'usuario_id', 'usuario_no',
                    'usuario_nombre', 'usuario_cargo', 'usuario_permisos'
                ]
                for key in keys_to_delete:
                    if key in request.session:
                        del request.session[key]

                # B. Enviamos el mensaje
                messages.warning(request,
                                 "⚠️ Tu sesión ha expirado por inactividad. Por favor, identifícate nuevamente.")

                # C. Redirigimos al Dashboard (que cargará MenuPrincipal.html)
                return redirect('dashboard')

                # 2. VERIFICAR PERMISOS (ROLES)
            permisos_sesion = request.session.get('usuario_permisos', '') or ''

            if rol_necesario in permisos_sesion or 'ADMIN' in permisos_sesion:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f"⛔ No tienes permisos de {rol_necesario} para entrar aquí.")
                return redirect('Menu principal')

        return _wrapped_view

    return decorator