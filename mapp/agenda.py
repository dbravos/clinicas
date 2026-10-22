"""
Agenda de internos por atender.

Cada vez que se cierra una sesión (consejería individual o familiar,
psicología o seguimiento) se captura la fecha de la siguiente. La agenda
toma, por interno y por tipo de sesión, la última sesión registrada: si está
cerrada y tiene próxima fecha, ese interno está pendiente de atender.

Cada profesional ve solo a sus pacientes (los de las sesiones que él
registró); administración ve a todos y puede filtrar por profesional.
"""
from datetime import date, timedelta

from django.shortcuts import redirect, render
from django.urls import reverse

from .models import CFamiliar, CIndividual, Internos, NotasEvolucionPS, NotasSeguimiento, Usuarios

DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

# (modelo, nombre visible, campo del profesional, campo con su nombre, cómo capturar la siguiente sesión)
TIPOS_SESION = [
    (CIndividual, 'Consejería individual', 'consejero', 'nombreconsejero',
     lambda exp: reverse('capturaSesion', kwargs={'tipo_sesion': 'individual', 'accion': 'agregar', 'id': exp})),
    (CFamiliar, 'Consejería familiar', 'consejero', 'nombreconsejero',
     lambda exp: reverse('capturaSesion', kwargs={'tipo_sesion': 'familiar', 'accion': 'agregar', 'id': exp})),
    (NotasEvolucionPS, 'Psicología', 'psicologo', 'nombrepsicologo',
     lambda exp: reverse('capturaSesionPS', kwargs={'accion': 'agregar', 'id': exp})),
    (NotasSeguimiento, 'Seguimiento', 'consejero', 'nombreconsejero',
     lambda exp: reverse('capturaSesionS', kwargs={'accion': 'agregar', 'id': exp})),
]


def citas_pendientes(clinica, profesional=None):
    """Lista de citas pendientes de la clínica, ordenadas por fecha.

    profesional: número de usuario para ver solo sus pacientes; None = todos.
    """
    # Solo internos activos (sin fecha de salida)
    internos = {
        i.numeroexpediente: i
        for i in Internos.objects.filter(clinica=clinica, fsalidareal__isnull=True)
    }
    hoy = date.today()
    citas = []
    for modelo, tipo, campo_prof, campo_nombre, url_captura in TIPOS_SESION:
        filas = (modelo.objects
                 .filter(clinica=clinica, expediente__in=internos.keys())
                 .order_by('expediente', '-sesion')
                 .values('expediente', 'sesion', 'status', 'proximasesion', campo_prof, campo_nombre))
        vistos = set()
        for f in filas:
            if f['expediente'] in vistos:
                continue                      # solo cuenta la última sesión de cada interno
            vistos.add(f['expediente'])
            if f['status'] != 1 or not f['proximasesion']:
                continue                      # sesión abierta o sin próxima fecha: nada pendiente
            if profesional is not None and f[campo_prof] != profesional:
                continue
            interno = internos[f['expediente']]
            citas.append({
                'fecha': f['proximasesion'],
                'dia': DIAS[f['proximasesion'].weekday()],
                'dia_corto': DIAS[f['proximasesion'].weekday()][:3],
                'dias': (f['proximasesion'] - hoy).days,   # negativo = vencida
                'dias_abs': abs((f['proximasesion'] - hoy).days),
                'tipo': tipo,
                'interno': interno,
                'ultima_sesion': f['sesion'],
                'profesional_no': f[campo_prof],
                'profesional': f[campo_nombre] or '—',
                'url_captura': url_captura(interno.numeroexpediente),
            })
    citas.sort(key=lambda c: (c['fecha'], c['interno'].nombrecompleto or ''))
    return citas


def agrupar(citas, hoy=None):
    hoy = hoy or date.today()
    en_7_dias = hoy + timedelta(days=7)
    grupos = {clave: {'clave': clave, 'titulo': titulo, 'citas': []}
              for clave, titulo in [('vencidas', 'Vencidas'), ('hoy', 'Hoy'),
                                    ('semana', 'Próximos 7 días'), ('despues', 'Más adelante')]}
    for c in citas:
        if c['fecha'] < hoy:
            clave = 'vencidas'
        elif c['fecha'] == hoy:
            clave = 'hoy'
        elif c['fecha'] <= en_7_dias:
            clave = 'semana'
        else:
            clave = 'despues'
        grupos[clave]['citas'].append(c)
    return list(grupos.values())


def resumen_para_usuario(request):
    """Conteo de vencidas + hoy para el usuario en sesión (aviso en Inicio)."""
    clinica = request.session.get('clinica_actual')
    if not clinica or not request.session.get('usuario_autenticado'):
        return 0
    es_admin = 'ADMIN' in (request.session.get('usuario_permisos') or '').upper()
    profesional = None if es_admin else request.session.get('usuario_no')
    hoy = date.today()
    return sum(1 for c in citas_pendientes(clinica, profesional) if c['fecha'] <= hoy)


def agenda(request):
    if 'clinica_actual' not in request.session:
        return redirect('login_clinica')
    if not request.session.get('usuario_autenticado'):
        return redirect('dashboard')          # ahí se pide la identificación del operador

    clinica = request.session['clinica_actual']
    es_admin = 'ADMIN' in (request.session.get('usuario_permisos') or '').upper()

    profesionales = []
    filtro = None
    if es_admin:
        profesionales = Usuarios.objects.filter(clinica=clinica).order_by('nombre')
        try:
            filtro = int(request.GET.get('profesional') or 0) or None
        except ValueError:
            filtro = None
        profesional = filtro
    else:
        profesional = request.session.get('usuario_no')

    citas = citas_pendientes(clinica, profesional)
    hoy = date.today()
    return render(request, 'agenda.html', {
        'grupos': agrupar(citas, hoy),
        'total': len(citas),
        'hoy': hoy,
        'es_admin': es_admin,
        'profesionales': profesionales,
        'filtro': filtro,
    })
