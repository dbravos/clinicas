from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import  Http404, HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction,DatabaseError
import logging
import json
import os
from reportlab.pdfgen import canvas  # ✅ AGREGAR ESTA IMPORTACIÓN
from reportlab.lib.pagesizes import letter  # ✅ Y ESTA TAMBIÉN
from datetime import  timedelta,datetime
from django.urls import reverse
import io
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from num2words import num2words  # pip install num2words
import io
import requests  # <--- Necesario para descargar la imagen de ImgBB
from reportlab.lib.utils import ImageReader
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Sum


# IMPORTS COMPATIBLES CON WINDOWS/LINUX
try:
    import pythoncom
    import win32com.client
    import win32print
    import win32api
    WINDOWS_SYSTEM = True
except ImportError:
    WINDOWS_SYSTEM = False
    # Alternativas para Linux (Railway)
    pythoncom = None
    win32com = None
    win32print = None
    win32api = None




from mapp.models import Internos,Usuarios,DatosGrales,Einicial,Assist,SituacionFamiliar,Cfisicas,Cmentales,\
                        Crelaciones,Tratamientos,Psicosis,Sdevida,Usodrogas,Ansiedad,Depresion,Marcadores,Riesgos,\
                        Razones,Valorizacion,CIndividual,CFamiliar,CGrupal,PConsejeria,TareaConsejeria,HojaAtencionPs,\
                        NotasEvolucionPS,Medico,Recetas,HistoriaClinica,Clinicas,Seguimiento,NotasSeguimiento,Edocuenta,\
                        Recibos

from .formas import DatosGralesf,Usuariosf,Internosf,IntResponsablef,IntDependientesf,IntProvienef,Einicialf,\
                    Assistf,SituacionFamiliarf,Cfisicasf,Cmentalesf,Crelacionesf,Tratamientosf,Psicosisf,Sdevidaf,\
                    Usodrogasf,Ansiedadf,Depresionf,Marcadoresf,Riesgosf,Razonesf,Valorizacionf,\
                    CIndividualf,CFamiliarf,CGrupalf,PConsejeriaf,TareaConsejeriaf,HojaAtencionPsf,NotasEvolucionPSf,\
                    Medicof,Recetasf,HistoriaClinicaf,ClinicaLoginForm,IntSalidasf,Seguimientof,NotasSeguimientof,\
                    ReporteFechaForm,Edocuentaf




logger = logging.getLogger(__name__)

# Create your views here.

def home_temp(request):
    return HttpResponse("¡Mi Django funciona en Railway! 🚀")

def get_clinica_actual(request):
    return request.session.get('clinica_actual', 'Demostracion')

def primermenu(request):
    interno = Internos.objects.first()
    return render(request,'MenuPrincipal.html', {'interno': interno})

def reporte_internos(request):
    return render(request,'reporte_internos.html')

def imprime_contrato(request,id):
    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.get(clinica=clinica_actual)

    return render(request,'imprime_contrato.html', {'interno': interno,'datosgrales':datosgrales})

def imprime_solicitud(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.get(clinica=clinica_actual)

    return render(request,'solicitud_internacion.html', {'interno': interno,'datosgrales':datosgrales})



def imprime_aviso(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id)

    # Usamos filter().first() es más seguro que get() por si acaso no existe el registro
    datosgrales = DatosGrales.objects.filter(clinica=clinica_actual).first()

    # --- 1. LÓGICA DE FECHA ---
    fecha_formateada = "FECHA NO DISPONIBLE"

    if interno.fechaingreso:
        meses = {
            1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
            5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
            9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
        }
        fecha_formateada = f"{interno.fechaingreso.day} de {meses[interno.fechaingreso.month]} del {interno.fechaingreso.year}"

    # --- 2. LÓGICA DE MÉDICOS (NUEVO) ---
    # Buscamos usuarios de esta clínica que tengan el cargo 'Medico'
    # IMPORTANTE: Revisa en tu base de datos si lo guardaste como 'Medico', 'MEDICO' o 'Médico'
    lista_medicos = Usuarios.objects.filter(
        clinica=clinica_actual,
        cargo='Medico'
    )

    # --- 3. CONTEXTO Y RENDER ---
    context = {
        'interno': interno,
        'datosgrales': datosgrales,
        'fecha_formateada': fecha_formateada,
        'medicos': lista_medicos  # <--- Enviamos la lista al template
    }

    return render(request, 'aviso_internacion.html', context)


# En tu vista de consentimiento
def consentimiento(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.get(clinica=clinica_actual)  # O como obtengas estos datos

    # Formatear fecha actual
    from django.utils import timezone
    fecha_actual = timezone.now().strftime('%d/%m/%Y %I:%M %p')

    contexto = {
        'interno': interno,
        'datosgrales': datosgrales,
        'fecha_actual': fecha_actual,
    }

    return render(request, 'carta_consentimiento.html', contexto)

def probar(request):
    return render(request,'agregar.html')

def listaint(request):
    clinica_actual=get_clinica_actual(request)
    internos = Internos.objects.filter(clinica=clinica_actual).order_by('numeroexpediente')
    return render(request, 'listar.html', {'internos': internos})


def agregainterno(request):
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    # Obtener la clínica actual de la sesión
    clinica_actual = request.session.get('clinica_actual', 'Demostracion')

    try:
        # 1. Obtener el último número de expediente DE LA CLÍNICA ACTUAL
        ultimo = Internos.objects.filter(clinica=clinica_actual).order_by('-numeroexpediente').first()

        # 2. Generar nuevo número consecutivo
        nuevo_numero = int(ultimo.numeroexpediente) + 1 if ultimo else 1
        numero_expediente = str(nuevo_numero).zfill(6)  # Formato 000001

        # 3. Crear el nuevo registro CON LA CLÍNICA
        interno = Internos.objects.create(
            numeroexpediente=numero_expediente,
            clinica=clinica_actual,  # ← ESTA LÍNEA ES CLAVE
            quieninformo=mem_user_nombre
        )

        internof = Internosf(instance=interno)
        intresponsablef = IntResponsablef(instance=interno)
        intdependientesf = IntDependientesf(instance=interno)
        intprovienef = IntProvienef(instance=interno)

        messages.success(request, f'Interno {numero_expediente} creado exitosamente en {clinica_actual}')
        return render(request, 'internosnw.html', {
            'interno': interno,
            'internof': internof,
            'intresponsablef': intresponsablef,
            'intdependientesf': intdependientesf,
            'intprovienef': intprovienef
        })

    except Exception as e:
        messages.error(request, f'Error al crear: {str(e)}')
        return redirect('listaint')


def seleccionainterno(request,id):
    interno = get_object_or_404(Internos, pk=id)
    opcion = request.GET.get('opcion', None)

    request.session['expediente_actual'] = interno.numeroexpediente
    request.session['interno_actual_id'] = interno.pk
    clinica_actual = get_clinica_actual(request)

    internof = Internosf(instance=interno)
    intresponsablef=IntResponsablef(instance=interno)
    intdependientesf=IntDependientesf(instance=interno)
    intprovienef=IntProvienef(instance=interno)
    if opcion=="editar":
       return render(request, 'internosnw.html', {'interno':interno,'internof':internof, 'intresponsablef':intresponsablef, 'intdependientesf':intdependientesf,'intprovienef':intprovienef })
    else:
       return render(request, 'dgenerales.html', {'interno':interno})

def borrainterno(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id, clinica=clinica_actual)
    interno.delete()
    messages.success(request, 'Interno de expediente  #' + str(id)+' borrado')
    internos = Internos.objects.filter(clinca=clinica_actual)
    return render(request, 'listar.html', {'internos': internos})



def grabainterno(request, id):
    clinica_actual = get_clinica_actual(request)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')
    # Usamos get_object_or_404 por seguridad
    interno = get_object_or_404(Internos, pk=id, clinica=clinica_actual)

    if request.method == 'POST':
        # Instanciamos los formularios con los datos del POST
        internof = Internosf(request.POST, instance=interno)
        intresponsablef = IntResponsablef(request.POST, instance=interno)
        intdependientesf = IntDependientesf(request.POST, instance=interno)
        intprovienef = IntProvienef(request.POST, instance=interno)

        # Validamos TODOS los formularios antes de intentar guardar nada
        if all([internof.is_valid(), intresponsablef.is_valid(), intdependientesf.is_valid(), intprovienef.is_valid()]):

            try:
                with transaction.atomic():
                    # 1. Actualizar campos manuales antes de guardar
                   # interno.nombrecompleto = f"{interno.nombre} {interno.apaterno} {interno.amaterno}"
                    interno.comentarios = request.POST.get('comentarios', '')

                    # 2. Guardar formularios (internof.save() ya guarda 'interno')
                    internof.save()
                    intresponsablef.save()
                    intdependientesf.save()
                    intprovienef.save()

                    # ==========================================================
                    # LÓGICA: GENERACIÓN DE CUOTAS
                    # ==========================================================
                    # Verificamos si el checkbox viene marcado ('true' o 'on' dependiendo del navegador, asumimos 'true' por tu script)
                    if request.POST.get('generar_cuotas') == 'true':

                        # Usamos los datos LIMPIOS del formulario validado, no del POST crudo (más seguro)
                        # O bien, usamos los del objeto 'interno' que ya se actualizó
                        saldo_pendiente = float(request.POST.get('saldo') or 0)
                        monto_cuota = float(request.POST.get('cuota') or 0)
                        fecha_str = request.POST.get('fecha_inicio_pago')
                        periodo_texto = str(interno.periodopago).upper()

                        # Validaciones de Cuotas
                        if saldo_pendiente <= 0 or monto_cuota <= 0:
                            messages.warning(request,
                                             "Datos guardados, pero NO se generaron cuotas: Saldo o Cuota en 0.")
                        elif not fecha_str:
                            messages.warning(request,
                                             "Datos guardados, pero NO se generaron cuotas: Falta fecha de inicio.")
                        else:
                            # Cálculos
                            fecha_actual = datetime.strptime(fecha_str, '%Y-%m-%d').date()

                            dias_sumar = 7  # Default
                            if 'CATORCENAL' in periodo_texto or '14' in periodo_texto:
                                dias_sumar = 14
                            elif 'QUINCENAL' in periodo_texto or '15' in periodo_texto:
                                dias_sumar = 15
                            elif 'MENSUAL' in periodo_texto or '30' in periodo_texto:
                                dias_sumar = 30

                            contador = 1
                            # Limite de seguridad
                            while saldo_pendiente > 0.1 and contador < 500:
                                pago_actual = saldo_pendiente if saldo_pendiente < monto_cuota else monto_cuota

                                Edocuenta.objects.create(
                                    expediente=interno.numeroexpediente,
                                    clinica=clinica_actual,
                                    fecha=fecha_actual,
                                    concepto=1,
                                    tipo='C',
                                    importe=pago_actual,
                                    referencia=f"Cuota # {contador}",
                                    operador=mem_user_no,
                                    nombreoperador=mem_user_nombre
                                )

                                saldo_pendiente -= pago_actual
                                fecha_actual = fecha_actual + timedelta(days=dias_sumar)
                                contador += 1

                            messages.success(request,
                                             f"Se actualizaron los datos y se programaron {contador - 1} cuotas.")
                    else:
                        messages.success(request,
                                         f'Actualización exitosa del expediente {interno.numeroexpediente} (Sin generar cuotas).')

            except Exception as e:
                # Si algo falla dentro del transaction.atomic, se deshace todo
                messages.error(request, f'Error crítico al guardar: {str(e)}')

        else:
            # Si los formularios no son válidos, mostramos qué falló
            errores = ""
            if not internof.is_valid(): errores += f"Generales: {internof.errors.as_text()} "
            if not intresponsablef.is_valid(): errores += f"Responsable: {intresponsablef.errors.as_text()} "
            messages.error(request, f'No se pudo guardar. Revise los errores: {errores}')

    # RECOMENDACIÓN: Después de un POST exitoso, usa redirect para evitar reenvío de formulario al refrescar.
    # Si prefieres quedarte en la misma vista, usa render.

    internos = Internos.objects.filter(clinica=clinica_actual).order_by('numeroexpediente')
    return render(request, 'listar.html', {'internos': internos})


def registro(request):
    return render(request,'registro.html')


def datosgrales(request):
    clinica_actual = get_clinica_actual(request)
    rol_usuario = request.session.get('usuario_permisos', None)
    try:
        datosgrales = DatosGrales.objects.get(clinica=clinica_actual)
    except DatosGrales.DoesNotExist:
        # Crear con MÍNIMOS campos requeridos
        datosgrales = DatosGrales(
            clinica=clinica_actual,
            nombre=clinica_actual,
        )
        print("Antes de save")  # Debug
        datosgrales.save()  # ← Si falla aquí, el problema está en el modelo
        print("Después de save")  # Debug

    datosgralesf = DatosGralesf(instance=datosgrales,permisos=rol_usuario)
    return render(request, 'datosgrales.html', {
        'datosgrales': datosgrales,
        'datosgralesf': datosgralesf
    })


def grabadatosgrales(request):
    clinica_actual = get_clinica_actual(request)

    try:
        datosgrales = DatosGrales.objects.get(clinica=clinica_actual)
    except DatosGrales.DoesNotExist:
        datosgrales = DatosGrales(clinica=clinica_actual)

    try:
        clinica = Clinicas.objects.get(clinica=clinica_actual)
    except Clinicas.DoesNotExist:
        clinica = Clinicas(clinica=clinica_actual)



    if request.method == 'POST':
        # DEBUG: Ver qué llega en el request

        rol_usuario = request.session.get('usuario_permisos', None)
        print(f"🔍 este es el rol del usuario {rol_usuario}")
        datosgralesf = DatosGralesf(request.POST,
                                    request.FILES,
                                    instance=datosgrales,
                                    permisos=rol_usuario,
                                    )

        if datosgralesf.is_valid():
            instance = datosgralesf.save(commit=False)
            nuevo_password = datosgralesf.cleaned_data.get('password')

            # Verificamos si existe (recuerda que si no es admin, el campo no existe)
            # y si el usuario escribió algo (para no borrarlo si lo deja en blanco)
            if nuevo_password:
                print(f"🔄 Sincronizando password en tabla Clinicas...")
                clinica.password = nuevo_password
                clinica.save()  # <-- IMPORTANTE: Guardar el cambio en la tabla Clinicas
                print("✅ Password de Clínica actualizado correctamente")

            # DEBUG: Verificar el campo específico
            print(f"🔍 Buscando 'logo_clinica' en FILES: {'logo_clinica' in request.FILES}")

            if 'logo_clinica' in request.FILES and request.FILES['logo_clinica']:
                print("🔄 EJECUTANDO ImgBB upload...")  # Este debe aparecer en logs
                try:
                    api_key = '8c061775423c7c7ffc99af2f3ed63c42'
                    files = {'image': request.FILES['logo_clinica']}

                    response = requests.post(
                        f"https://api.imgbb.com/1/upload?key={api_key}",
                        files=files
                    )
                    print(f"📡 Status Code ImgBB: {response.status_code}")

                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ URL ImgBB: {result['data']['url']}")
                        instance.logo_url = result['data']['url']
                    else:
                        print(f"❌ Error ImgBB: {response.text}")

                except Exception as e:
                    print(f"💥 Excepción: {e}")
            else:
                print("❌ No se encontró logo_clinica en FILES")

            instance.save()
            return redirect('datosgrales')
        else:
            print(f"❌ Formulario inválido: {datosgralesf.errors}")

    return redirect('datosgrales')


def lusuarios(request):
    clinica_actual = get_clinica_actual(request)
    usuarios = Usuarios.objects.filter(clinica=clinica_actual)

    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos').upper()

    if not 'ADMIN' in mem_user_permisos:
       messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
       return redirect('Menu principal')

    context = {'usuarios': usuarios,
               'mem_user_no':mem_user_no,
               'mem_user_nombre': mem_user_nombre,
               'mem_user_permisos': mem_user_permisos
               }
    return render(request, 'lusuarios.html', context)


def agregausuario(request):
    clinica_actual = get_clinica_actual(request)

    # Calcular el próximo número de usuario
    ultimo_usuario = Usuarios.objects.filter(clinica=clinica_actual).order_by('-usuario').first()
    nuevo_numero = (ultimo_usuario.usuario + 1) if ultimo_usuario else 1

    # Crear usuario con get_or_create
    usuario, created = Usuarios.objects.get_or_create(
        usuario=nuevo_numero,
        clinica=clinica_actual,
        defaults={
            'nombre': f'Usuario {nuevo_numero}',
            'password': '123456',  # Password por defecto
            'permisos': 'user',  # Permiso por defecto
            'cargo': '',
            'cedula': '',
            'expedidapor': ''
        }
    )

    usuariof = Usuariosf(instance=usuario)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')


    context = {
        'usuario': usuario,
        'usuariof': usuariof,
        'mem_user_no': mem_user_no,
        'mem_user_nombre': mem_user_nombre,
        'mem_user_permisos': mem_user_permisos
    }

    return render(request, 'usuarios.html', context)


def grabadatosusuario(request, id):
    clinica_actual = get_clinica_actual(request)

    # Usamos get_object_or_404 para evitar error 500 si el usuario no existe
    usuario = get_object_or_404(Usuarios, usuario=id, clinica=clinica_actual)

    # 1. GUARDAMOS LA CONTRASEÑA ACTUAL EN UNA VARIABLE TEMPORAL
    password_anterior = usuario.password

    if request.method == 'POST':
        usuariof = Usuariosf(request.POST, instance=usuario)

        if usuariof.is_valid():
            # 2. PAUSA EL GUARDADO (commit=False)
            usuario_editado = usuariof.save(commit=False)

            # 3. VERIFICAR SI ESCRIBIERON PASSWORD
            nueva_pass = usuariof.cleaned_data.get('password')

            if not nueva_pass:
                # Si está vacío, le volvemos a poner la contraseña vieja
                usuario_editado.password = password_anterior
            else:
                # Si escribieron algo, se queda la nueva (ya está en usuario_editado)
                pass

                # 4. AHORA SÍ GUARDAMOS EN LA BD
            usuario_editado.save()

            messages.success(request, 'Actualización exitosa del usuario ' + str(usuario.usuario))
        else:
            # Es bueno mostrar los errores del formulario
            messages.error(request, f'No se actualizó {id}. Errores: {usuariof.errors}')

    # -------------------------------------------------------------
    # RECARGAR LA LISTA (Igual que como lo tenías)
    # -------------------------------------------------------------
    usuarios = Usuarios.objects.filter(clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    context = {
        'usuarios': usuarios,
        'mem_user_no': mem_user_no,
        'mem_user_nombre': mem_user_nombre,
        'mem_user_permisos': mem_user_permisos
    }

    return render(request, 'lusuarios.html', context)


def editausuario(request,id):

    clinica_actual=get_clinica_actual(request)
    usuario = get_object_or_404(Usuarios, pk=id,clinica=clinica_actual)
    usuariof = Usuariosf(instance=usuario)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    context = {'usuario': usuario,
               'usuariof': usuariof,
               'mem_user_no': mem_user_no,
               'mem_user_nombre': mem_user_nombre,
               'mem_user_permisos': mem_user_permisos
               }

    return render(request, 'usuarios.html', context)

def borrausuario(request,id):
    clinica_actual=get_clinica_actual(request)
    usuario = get_object_or_404(Usuarios, usuario=id,clinica=clinica_actual)
    usuario.delete()
    messages.success(request, 'Usuario #' + str(usuario.usuario)+' borrado')
    usuarios = Usuarios.objects.filter(clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    context = {'usuarios': usuarios,
               'mem_user_no': mem_user_no,
               'mem_user_nombre': mem_user_nombre,
               'mem_user_permisos': mem_user_permisos
               }

    return render(request, 'lusuarios.html', context)




def einicial(request, id):
    clinica_actual = get_clinica_actual(request)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')
    if not 'CONSEJERIA' in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')
    # Obtener el interno
    interno = get_object_or_404(Internos, pk=id, clinica=clinica_actual)

    # Diccionario con los valores por defecto
    defaults = {
        'expediente': interno.numeroexpediente,
        'consejero': mem_user_no,
        'nombreconsejero': mem_user_nombre,
        'clinica': clinica_actual
    }

    # Crear registros con get_or_create (esto SÍ aplica defaults al crear)
    einicial, created = Einicial.objects.get_or_create(
        expediente=interno.numeroexpediente,
        clinica=clinica_actual,
        defaults=defaults
    )

    situacionfamiliar, created = SituacionFamiliar.objects.get_or_create(
        expediente=interno.numeroexpediente,
        clinica=clinica_actual,
        defaults=defaults
    )

    cfisicas, created = Cfisicas.objects.get_or_create(
        expediente=interno.numeroexpediente,
        clinica=clinica_actual,
        defaults=defaults
    )

    cmentales, created = Cmentales.objects.get_or_create(
        expediente=interno.numeroexpediente,
        clinica=clinica_actual,
        defaults=defaults
    )

    crelaciones, created = Crelaciones.objects.get_or_create(
        expediente=interno.numeroexpediente,
        clinica=clinica_actual,
        defaults=defaults
    )

    tratamientos, created = Tratamientos.objects.get_or_create(
        expediente=interno.numeroexpediente,
        clinica=clinica_actual,
        defaults=defaults
    )

    valorizacion, created = Valorizacion.objects.get_or_create(
        expediente=interno.numeroexpediente,
        clinica=clinica_actual,

    )

    # CREAR FORMULARIOS UNA SOLA VEZ (fuera del if POST)
    einicialf = Einicialf(request.POST or None, instance=einicial)
    situacionfamiliarf = SituacionFamiliarf(request.POST or None, instance=situacionfamiliar)
    cfisicasf = Cfisicasf(request.POST or None, instance=cfisicas)
    cmentalesf = Cmentalesf(request.POST or None, instance=cmentales)
    crelacionesf = Crelacionesf(request.POST or None, instance=crelaciones)
    tratamientosf = Tratamientosf(request.POST or None, instance=tratamientos)
    valorizacionf = Valorizacionf(request.POST or None, instance=valorizacion)

    # Manejo de POST
    if request.method == "POST":
        if all(form.is_valid() for form in
               [einicialf, situacionfamiliarf, cfisicasf, cmentalesf, crelacionesf, tratamientosf, valorizacionf]):
            try:
                with transaction.atomic():
                    einicialf.save()
                    situacionfamiliarf.save()
                    cfisicasf.save()
                    cmentalesf.save()
                    crelacionesf.save()
                    tratamientosf.save()
                    valorizacionf.save()

                messages.success(request, 'Datos actualizados correctamente')
                return redirect('einicial', id=id)
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
        else:
            for form in [einicialf, situacionfamiliarf, cfisicasf, cmentalesf, crelacionesf, tratamientosf,
                         valorizacionf]:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error en {form.__class__.__name__} - {field}: {error}")

    situaciones = [
        ('edesagradables', 'Emociones desagradables (triste, ansioso, etc.)'),
        ('enfermedad', 'Por alguna enfermedad'),
        ('eagradables', 'Emociones agradables (feliz, contento, etc.)'),
        ('necesidadfisica', 'Necesidad física (síndrome de abstinencia)'),
        ('probando', 'Probando autocontrol'),
        ('conflictos', 'Conflictos con otros'),
        ('agradablesotros', 'Momentos agradables con otros'),
        ('presion', 'Presión social')
    ]

    context = {
        'interno': interno,
        'einicialf': einicialf,
        'situacionfamiliarf': situacionfamiliarf,
        'cfisicasf': cfisicasf,
        'cmentalesf': cmentalesf,
        'crelacionesf': crelacionesf,
        'tratamientosf': tratamientosf,
        'valorizacionf': valorizacionf,
        'situaciones': situaciones
    }
    return render(request, 'einicialnw.html', context)



def grabaeinicial(request, id):
    """Vista simplificada solo para ACTUALIZAR registros existentes"""
    clinica_actual = get_clinica_actual(request)

    try:
        interno = get_object_or_404(Internos, pk=id, clinica=clinica_actual)

        if not interno.numeroexpediente:
            messages.error(request, "El interno no tiene número de expediente asignado")
            return redirect('selecciona')

        # OBTENER instancias existentes (NO crear)
        instancias = {
            'einicial': get_object_or_404(Einicial, expediente=interno.numeroexpediente, clinica=clinica_actual),
            'situacionfamiliar': get_object_or_404(SituacionFamiliar, expediente=interno.numeroexpediente,
                                                   clinica=clinica_actual),
            'cfisicas': get_object_or_404(Cfisicas, expediente=interno.numeroexpediente, clinica=clinica_actual),
            'cmentales': get_object_or_404(Cmentales, expediente=interno.numeroexpediente, clinica=clinica_actual),
            'crelaciones': get_object_or_404(Crelaciones, expediente=interno.numeroexpediente, clinica=clinica_actual),
            'tratamientos': get_object_or_404(Tratamientos, expediente=interno.numeroexpediente,
                                              clinica=clinica_actual),
        }

        # Crear formularios con las instancias
        forms = {
            'einicialf': Einicialf(request.POST or None, instance=instancias['einicial']),
            'situacionfamiliarf': SituacionFamiliarf(request.POST or None, instance=instancias['situacionfamiliar']),
            'cfisicasf': Cfisicasf(request.POST or None, instance=instancias['cfisicas']),
            'cmentalesf': Cmentalesf(request.POST or None, instance=instancias['cmentales']),
            'crelacionesf': Crelacionesf(request.POST or None, instance=instancias['crelaciones']),
            'tratamientosf': Tratamientosf(request.POST or None, instance=instancias['tratamientos'])
        }

        if request.method == "POST":
            if all(form.is_valid() for form in forms.values()):
                try:
                    with transaction.atomic():
                        for form in forms.values():
                            form.save()  # Solo guardar, los campos ya están en la instancia

                    messages.success(request, 'Datos actualizados correctamente')
                    return redirect('einicial', id=id)

                except Exception as e:
                    messages.error(request, f"Error al guardar: {str(e)}")
                    logger.exception("Error al guardar formularios")
            else:
                for form_name, form in forms.items():
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"Error en {form_name} - {field}: {error}")

        context = {
            'interno': interno,
            **forms
        }
        return render(request, 'einicialnw.html', context)

    except Exception as e:
        messages.error(request, "Error: Los registros iniciales no existen. Debe crearlos primero.")
        logger.error(f"Error en grabaeinicial: {str(e)}")
        return redirect('einicial', id=id)

def assist(request,id):

    clinica_actual=get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')
    if not 'CONSEJERIA' in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    try:
        assist = Assist.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        assistf = Assistf(instance=assist)

    except Assist.DoesNotExist:
        assist = Assist(expediente=interno.numeroexpediente)
        assist.consejero = mem_user_no
        assist.clinica = clinica_actual
        assist.nombreconsejero = mem_user_nombre
        assist.save()
        assistf = Assistf(instance=assist)
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        valorizacionf = Valorizacionf(instance=valorizacion)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion(expediente=interno.numeroexpediente)
        valorizacion.clinica=clinica_actual
        valorizacion.valorizacionnombreconsejero=mem_user_nombre
        valorizacion.valorizacionconsejero=mem_user_no
        valorizacion.save()
        valorizacionf = Valorizacionf(instance=valorizacion)

    if request.method == "POST":
        assistf = Assistf(request.POST, instance=assist)
        valorizacionf = Valorizacionf(instance=valorizacion)  # Solo para mostrar

        if assistf.is_valid():
            assistf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')

    return render(request, 'assist.html', {'assist': assist, 'assistf':assistf,'interno':interno,'valorizacion':valorizacion,'valorizacionf':valorizacionf} )

def grabalo(request, id):

    clinica_actual = get_clinica_actual(request)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    try:
        interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)

        if not interno.numeroexpediente:
            messages.error(request, "El interno no tiene número de expediente asignado")
            return redirect('selecciona')

        modelos = {
            'assist': Assist

        }

        with transaction.atomic():
            instancias = {}
            for nombre_modelo, modelo in modelos.items():
                try:
                    instancia, created = modelo.objects.get_or_create(
                        expediente=interno.numeroexpediente,
                        clinica=clinica_actual,
                        defaults={'expediente': interno.numeroexpediente,
                                  'clinica':clinica_actual,
                                  'consejero':mem_user_no,
                                  'nombreconsejero':mem_user_nombre}
                    )
                    if created:
                        instancia.full_clean()
                        instancia.save()
                    instancias[nombre_modelo] = instancia
                except Exception as e:
                    logger.error(f"Error creando {nombre_modelo}: {str(e)}")
                    raise

        forms = {
            'assistf': Assistf(request.POST or None, instance=instancias['assist'])
              }



        if request.method == "POST":

            print("Datos del formulario:", request.POST)
            if all(form.is_valid() for form in forms.values()):
                try:
                    with transaction.atomic():
                        for form in forms.values():
                            form.instance.expediente=interno.numeroexpediente
                            form.instance.clinica=clinica_actual
                            form.save()
                    messages.success(request, 'Datos guardados correctamente')
                    return redirect('assist', id=id)
                except Exception as e:
                    messages.error(request, f"Error al guardar: {str(e)}")
                    logger.exception("Error al guardar formularios")
            else:
                for form_name, form in forms.items():
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"Error en {form_name} - {field}: {error}")



        context = {
            'interno': interno,
            **forms,
            **instancias

        }
        return render(request, 'assist.html', context)

    except DatabaseError as e:
        messages.error(request, "Error de base de datos. Contacte al administrador.")
        logger.error(f"DatabaseError: {str(e)}")
        return redirect('assist', id=id)
    except ValidationError as e:
        messages.error(request, f"Error de validación: {str(e)}")
        logger.error(f"ValidationError: {e.message_dict}")
        return redirect('assist', id=id)
    except Exception as e:
         error_details = {
              'exception_type': type(e).__name__,
              'error_message': str(e),
              'form_errors': {name: form.errors.as_json() for name, form in forms.items() if hasattr(form, 'errors')},
              'post_data': request.POST.dict()
               }
         logger.exception(f"ERROR DETALLADO: {json.dumps(error_details, indent=2)}")
         messages.error(request, f"Error crítico en el formulario. Ver logs para detalles.")
         return redirect('assist', id=id)


def psicosis(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id, clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')
    if not 'CONSEJERIA' in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    try:
        psicosis_obj = Psicosis.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Psicosis.DoesNotExist:
        psicosis_obj = Psicosis(
            expediente=interno.numeroexpediente,
            psconsejero=mem_user_no,
            psnombreconsejero=mem_user_nombre,
            clinica=clinica_actual
        )
        psicosis_obj.save()


    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no,
            valorizacionnombreconsejero=mem_user_nombre
        )
        valorizacion.save()

    psicosisf = Psicosisf(instance=psicosis_obj)
    valorizacionf = Valorizacionf(instance=valorizacion)
    # 👇 MANEJAR POST EN LA MISMA VISTA
    if request.method == "POST":
        psicosisf = Psicosisf(request.POST, instance=psicosis_obj)
        valorizacionf = Valorizacionf(instance=valorizacion)  # Solo para mostrar

        if psicosisf.is_valid():
            psicosisf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')


    return render(request, 'psicosis.html', {
        'psicosis': psicosis_obj,
        'psicosisf': psicosisf,
        'interno': interno,
        'valorizacion': valorizacion,
        'valorizacionf': valorizacionf
    })

def sdevida(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id, clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')
    # Sdevida - obtener o crear
    try:
        sdevida = Sdevida.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Sdevida.DoesNotExist:
        sdevida = Sdevida.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            svconsejero=mem_user_no,
            svnombreconsejero=mem_user_nombre
        )
    sdevidaf = Sdevidaf(instance=sdevida)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no,
            valorizacionnombreconsejero=mem_user_nombre
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

    if request.method == "POST":
        sdevidaf = Sdevidaf(request.POST, instance=sdevida)
        valorizacionf = Valorizacionf(instance=valorizacion)  # Solo para mostrar

        if sdevidaf.is_valid():
            sdevidaf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')


    return render(request, 'satisfaccion.html', {
        'sdevida': sdevida,
        'sdevidaf': sdevidaf,
        'interno': interno,
        'valorizacion': valorizacion,
        'valorizacionf': valorizacionf
    })

def usodrogas(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id, clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')
    # Usodrogas - obtener o crear
    try:
        usodrogas = Usodrogas.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Usodrogas.DoesNotExist:
        usodrogas = Usodrogas.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            udconsejero=mem_user_no,
            udnombreconsejero=mem_user_nombre

        )
    usodrogasf = Usodrogasf(instance=usodrogas)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no,
            valorizacionnombreconsejero=mem_user_nombre
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

    if request.method == "POST":
        usodrogasf = Usodrogasf(request.POST, instance=usodrogas)
        valorizacionf = Valorizacionf(instance=valorizacion)  # Solo para mostrar

        if usodrogasf.is_valid():
            usodrogasf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')

    return render(request, 'usodrogas.html', {
        'usodrogas': usodrogas,
        'usodrogasf': usodrogasf,
        'interno': interno,
        'valorizacion': valorizacion,
        'valorizacionf': valorizacionf
    })



def ansiedad(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id, clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')
    # Ansiedad - obtener o crear
    try:
        ansiedad = Ansiedad.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Ansiedad.DoesNotExist:
        ansiedad = Ansiedad.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            anconsejero=mem_user_no,
            annombreconsejero=mem_user_nombre
        )
    ansiedadf = Ansiedadf(instance=ansiedad)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no,
            valorizacionnombreconsejero=mem_user_nombre
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

    if request.method == "POST":
        ansiedadf = Ansiedadf(request.POST, instance=ansiedad)
        valorizacionf = Valorizacionf(instance=valorizacion)  # Solo para mostrar

        if ansiedadf.is_valid():
            ansiedadf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')

    return render(request, 'ansiedad.html', {
        'ansiedad': ansiedad,
        'ansiedadf': ansiedadf,
        'interno': interno,
        'valorizacion': valorizacion,
        'valorizacionf': valorizacionf
    })


def depresion(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id, clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')
    # Depresion - obtener o crear
    try:
        depresion = Depresion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Depresion.DoesNotExist:
        depresion = Depresion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            depconsejero=mem_user_no,
            depnombreconsejero=mem_user_nombre
        )
    depresionf = Depresionf(instance=depresion)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no,
            valorizacionnombreconsejero=mem_user_nombre
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

    if request.method == "POST":
        depresionf = Depresionf(request.POST, instance=depresion)
        valorizacionf = Valorizacionf(instance=valorizacion)  # Solo para mostrar

        if depresionf.is_valid():
            depresionf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')

    return render(request, 'depresion.html', {
        'depresion': depresion,
        'depresionf': depresionf,
        'interno': interno,
        'valorizacion': valorizacion,
        'valorizacionf': valorizacionf  # ← CORREGÍ: estaba 'valorizacion' sin la 'f'
    })



def marcadores(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')
    try:
        marcadores = Marcadores.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        marcadoresf = Marcadoresf(instance=marcadores)
    except Marcadores.DoesNotExist:
        marcadores=Marcadores(expediente=interno.numeroexpediente)
        marcadores.marconsejero = mem_user_no
        marcadores.marnombreconsejero = mem_user_nombre
        marcadores.clinica = clinica_actual
        marcadores.save()
        marcadoresf=Marcadoresf(instance=marcadores)

    if request.method == "POST":
        marcadoresf = Marcadoresf(request.POST, instance=marcadores)

        if marcadoresf.is_valid():
            marcadoresf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')
    return render(request, 'marcadores.html', {'marcadores': marcadores, 'marcadoresf':marcadoresf,'interno':interno} )

def riesgos(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    try:
        riesgos = Riesgos.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        riesgosf = Riesgosf(instance=riesgos)
    except Riesgos.DoesNotExist:
        riesgos=Riesgos(expediente=interno.numeroexpediente)
        riesgos.riesgoconsejero = mem_user_no
        riesgos.riesgonombreconsejero = mem_user_nombre
        riesgos.clinica = clinica_actual
        riesgos.save()
        riesgosf=Riesgosf(instance=riesgos)

    if request.method == "POST":
        riesgosf = Riesgosf(request.POST, instance=riesgos)

        if riesgosf.is_valid():
            riesgosf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')


    return render(request, 'riesgos.html', {'riesgos': riesgos, 'riesgosf':riesgosf,'interno':interno} )

def razones(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    try:
        razones = Razones.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        razonesf = Razonesf(instance=razones)
    except Razones.DoesNotExist:
        razones=Razones(expediente=interno.numeroexpediente)
        razones.razonesconsejero = mem_user_no
        razones.razonesnombreconsejero = mem_user_nombre
        razones.clinica = clinica_actual
        razones.save()
        razonesf=Razonesf(instance=razones)

    if request.method == "POST":
        razonesf = Razonesf(request.POST, instance=razones)

        if razonesf.is_valid():
            razonesf.save()
            messages.success(request, 'Datos guardados correctamente')
            return redirect('seleccionainterno', id=id)
        else:
            messages.error(request, 'Error al guardar los datos')

    return render(request, 'razones.html', {'razones': razones, 'razonesf':razonesf,'interno':interno} )


def salidas(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id, clinica=clinica_actual)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    if request.method == 'POST':
        form = IntSalidasf(request.POST, instance=interno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salida del interno registrada exitosamente')
            # Recarga la misma página para ver los datos actualizados
            return redirect('salidas', id=id)
    else:
        form = IntSalidasf(instance=interno)

    return render(request, 'salidas.html', {
        'form': form,
        'interno': interno
    })


def valorizacion(request,id):

    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        valorizacionf = Valorizacionf(instance=valorizacion)
    except Valorizacion.DoesNotExist:
        valorizacion=Valorizacion(expediente=interno.numeroexpediente)
        valorizacion.clinica = clinica_actual
        valorizacion.save()
        valorizacionf=Valorizacionf(instance=valorizacion)

    try:
        einicial = get_object_or_404(Einicial, expediente=interno.numeroexpediente,clinica=clinica_actual)
        eincialf =  Einicialf(instance=einicial)
        valorizacion.cantidadpromedio=einicial.cantidadpromedio
        valorizacion.hacecuanto=einicial.hacecuanto
        valorizacion.mainsustance=einicial.principalsustancia
        valorizacion.razon1=einicial.razon1
        valorizacion.razon2=einicial.razon2
        valorizacion.razon3=einicial.razon3
        valorizacion.save()
        valorizacionf=Valorizacionf(instance=valorizacion)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Entrevistas Iniciales')
        return render(request, 'dgenerales.html', {'interno': interno})

    try:
        cfisicas = get_object_or_404(Cfisicas, expediente=interno.numeroexpediente,clinica=clinica_actual)
        cfisicasf = Cfisicasf(instance=cfisicas)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Consecuencias fisicas')
        return render(request, 'dgenerales.html', {'interno': interno})
    try:
        cmentales = get_object_or_404(Cmentales, expediente=interno.numeroexpediente,clinica=clinica_actual)
        cmentalesf = Cmentalesf(instance=cmentales)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Consecuencias fisicas')
        return render(request, 'dgenerales.html', {'interno': interno})

    try:
        crelaciones = get_object_or_404(Crelaciones, expediente=interno.numeroexpediente,clinica=clinica_actual)
        crelacionesf = Crelacionesf(instance=crelaciones)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Consecuencias en Relaciones')
        return render(request, 'dgenerales.html', {'interno': interno})

    try:
        psicosis = get_object_or_404(Psicosis, expediente=interno.numeroexpediente,clinica=clinica_actual)
        psicosisf = Psicosisf(instance=psicosis)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Psicosis')
        return render(request, 'dgenerales.html', {'interno': interno})
    try:
        assist = get_object_or_404(Assist, expediente=interno.numeroexpediente,clinica=clinica_actual)
        assistf = Assistf(instance=assist)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en ASSIST')
        return render(request, 'dgenerales.html', {'interno': interno})

    try:
        ansiedad = get_object_or_404(Ansiedad, expediente=interno.numeroexpediente,clinica=clinica_actual)
        ansiedadf = Ansiedadf(instance=ansiedad)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Ansiedad')
        return render(request, 'dgenerales.html', {'interno': interno})
    try:
        depresion = get_object_or_404(Depresion, expediente=interno.numeroexpediente,clinica=clinica_actual)
        depresionf = Depresionf(instance=depresion)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Depresion')
        return render(request, 'dgenerales.html', {'interno': interno})
    try:
        sdevida = get_object_or_404(Sdevida, expediente=interno.numeroexpediente,clinica=clinica_actual)
        sdevidaf = Depresionf(instance=sdevida)
    except Http404:
        messages.error(request, f'Interno {interno.numeroexpediente} no existe en Satisfaccion de Vida')
        return render(request, 'dgenerales.html', {'interno': interno})


    context = {'valorizacion': valorizacion,
               'valorizacionf': valorizacionf,
               'interno': interno,
               'cfisicas': cfisicas,
               'cmentales': cmentales,
               'crelaciones': crelaciones,
               'einicial': einicial,
               'psicosis': psicosis,
               'psicosisf': psicosisf,
               'assist': assist,
               'assistf': assistf,
               'ansiedad': ansiedad,
               'ansieadf': ansiedadf,
               'depresion': depresion,
               'depresionf': depresionf,
               'sdevida':sdevida,
               'sdevidaf':sdevidaf,

               }

    return render(request, 'valorizacion.html', context )

# en tu archivo de vistas


MODEL_FORM_MAP = {
    'individual': {'model': CIndividual, 'form_class':CIndividualf,'verbose_name': 'Individuales'},
    'familiar': {'model': CFamiliar, 'form_class':CFamiliarf,'verbose_name': 'Familiares'},
    'grupal': {'model': CGrupal, 'form_class':CGrupalf,'verbose_name': 'Grupales'},
}


def listaSesiones(request, tipo_sesion, id):
    """
    Lista sesiones (individuales, familiares o grupales) usando objects.raw.
    Puede filtrar por expediente si se proporciona expediente_id.
    """

    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    interno = Internos.objects.get(numeroexpediente=id, clinica=clinica_actual)
    mapping = MODEL_FORM_MAP.get(tipo_sesion)
    if not mapping:
        return render(request, 'error.html', {'message': 'Tipo de sesión no válido.'})

    modelo = mapping['model']
    verbose_name = mapping['verbose_name']
    form_class = mapping['form_class']
    form = form_class

    sesiones = modelo.objects.filter(expediente=id, clinica=clinica_actual).order_by('sesion')
    cuantas_sesiones = sesiones.count()
    ultima_sesion = sesiones.last()
    cerrada = False

    if ultima_sesion:
        como_esta = ultima_sesion.status
        if como_esta == 1:
            cerrada = True

    context = {
        'sesiones': sesiones,
        'tipo_sesion': tipo_sesion,
        'verbose_name': verbose_name,
        'id': id,
        'cuantas_sesiones': cuantas_sesiones,
        'cerrada': cerrada,
        'modelo': modelo,
        'form':form_class,
        'interno':interno,
    }
    return render(request, 'lista_sesiones.html', context)


from datetime import date


def capturaSesion(request, tipo_sesion, accion, id=None, no_sesion=None):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(numeroexpediente=id, clinica=clinica_actual)

    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

    if id is None and 'interno_actual_id' in request.session:
        id = request.session['interno_actual_id']

    mapping = MODEL_FORM_MAP.get(tipo_sesion)
    if not mapping:
        return render(request, 'error.html', {'message': 'Tipo de sesión no válido.'})

    modelo = mapping['model']
    verbose_name = mapping['verbose_name']
    form_class = mapping['form_class']

    cuantas_sesiones = 0
    nueva_sesion = 1
    cerrada = True
    ultima_sesion_obj = None
    instancia_sesion = None

    if accion == 'agregar':
       sesiones_existentes = modelo.objects.filter(expediente=interno.numeroexpediente,
                                                    clinica=clinica_actual).order_by('sesion')
       cuantas_sesiones = sesiones_existentes.count()

       if sesiones_existentes:
            ultima_sesion_obj = sesiones_existentes.last()
            nueva_sesion = ultima_sesion_obj.sesion + 1
            print(f"   Última sesión: {ultima_sesion_obj.sesion}")
            print(f"   Nueva sesión: {nueva_sesion}")
            if ultima_sesion_obj.status == 1:
                cerrada = True
            else:
                cerrada = False
            if not cerrada:
                messages.error(request, 'La sesión anterior no está cerrada por lo tanto no puede crear una nueva.')
                return redirect('listaSesiones', tipo_sesion=tipo_sesion, id=id)
       else:
            nueva_sesion = 1  # ← ESTA LÍNEA FALTA EN TU CÓDIGO
            print(f"   No hay sesiones, nueva sesión: {nueva_sesion}")




    if accion == 'editar' and no_sesion is not None:
        try:
            instancia_sesion = modelo.objects.get(pk=no_sesion)
            nueva_sesion = instancia_sesion.sesion
            cerrada = (instancia_sesion.status == 1)
        except modelo.DoesNotExist:
            messages.error(request, f'{verbose_name} a editar no encontrada.')
            return redirect('listaSesiones', tipo_sesion=tipo_sesion, id=interno.pk)
    else:
        instancia_sesion = None

    if request.method == 'POST':
        form = form_class(request.POST, instance=instancia_sesion)

        if form.is_valid():
            sesion_guardar = form.save(commit=False)
            sesion_guardar.expediente = interno.numeroexpediente
            sesion_guardar.consejero = mem_user_no
            sesion_guardar.nombreconsejero = mem_user_nombre
            sesion_guardar.clinica = clinica_actual

            # VALIDACIÓN DE FECHAS
            if accion == 'editar' and request.POST.get('status') == '1':
                proximasesion_str = request.POST.get('proximasesion')
                error_validacion = None
                if not proximasesion_str:
                    error_validacion = 'Error: Debe especificar una fecha para la próxima sesión al cerrar la sesión actual'
                elif proximasesion_str:
                    from datetime import datetime
                    try:
                        proximasesion = datetime.strptime(proximasesion_str, '%Y-%m-%d').date()
                        if proximasesion <= sesion_guardar.fecha:
                            error_validacion = f'Error: La próxima sesión debe ser posterior a la fecha de esta sesión ({sesion_guardar.fecha.strftime("%d/%m/%Y")})'
                        elif proximasesion < date.today():
                            error_validacion = 'Error: La próxima sesión no puede ser una fecha pasada'
                    except ValueError:
                        error_validacion = 'Error: Formato de fecha inválido'

                if error_validacion:
                    messages.error(request, error_validacion)
                    context = {
                        'form': form,
                        'id_expediente': id,
                        'numero_expediente': interno.numeroexpediente,
                        'numero_sesion_actual': nueva_sesion,
                        'tipo_sesion': tipo_sesion,
                        'verbose_name': verbose_name,
                        'interno': interno,
                        'cuantas_sesiones': cuantas_sesiones,
                        'cerrada': cerrada,
                        'ultima_sesion': ultima_sesion_obj,
                        'accion': accion,
                        'instancia_sesion': instancia_sesion,
                    }
                    return render(request, 'captura_sesion.html', context)

            if accion == 'agregar':
                sesion_guardar.sesion = nueva_sesion

            try:
                sesion_guardar.save()
                messages.success(request, f'{verbose_name} {sesion_guardar.sesion} guardada exitosamente.')
                return redirect('listaSesiones', tipo_sesion=tipo_sesion, id=id)
            except Exception as e:
                print(f"❌ ERROR AL GUARDAR: {e}")
                messages.error(request, f'Error al guardar: {e}')
        else:
            # 🔍 DEBUG DETALLADO DE ERRORES
            print("❌ FORMULARIO NO VÁLIDO:")
            for field, errors in form.errors.items():
                print(f"   - {field}: {errors}")
            messages.error(request, 'Error al guardar la sesión. Revisa los campos.')
    else:
        if instancia_sesion:
            form = form_class(instance=instancia_sesion)
        else:
            form = form_class(initial={
                'fecha': date.today(),
                'proximasesion': date.today() + timedelta(days=7)
            })

    context = {
        'form': form,
        'id_expediente': id,
        'numero_expediente': interno.numeroexpediente,
        'numero_sesion_actual': nueva_sesion,
        'tipo_sesion': tipo_sesion,
        'verbose_name': verbose_name,
        'interno': interno,
        'cuantas_sesiones': cuantas_sesiones,
        'cerrada': cerrada,
        'ultima_sesion': ultima_sesion_obj,
        'accion': accion,
        'instancia_sesion': instancia_sesion,
    }

    return render(request, 'captura_sesion.html', context)




def capturaSesionGrupal(request, tipo_sesion, accion, id=None, no_sesion=None):
    """
    Vista para capturar sesiones grupales - CON VALIDACIÓN CORREGIDA
    """
    clinica_actual=get_clinica_actual(request)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    internos_disponibles = Internos.objects.filter(clinica=clinica_actual).order_by('numeroexpediente')
    instancia_sesion = None

    interno_actual_id = request.session.get('interno_actual_id', 1)

    if accion == 'editar' and no_sesion:
        instancia_sesion = get_object_or_404(CGrupal, pk=no_sesion,clinica=clinica_actual)

    participantes_seleccionados = []
    if instancia_sesion:
        participantes_seleccionados = instancia_sesion.participantes.all()

    if request.method == 'POST':
        form = CGrupalf(request.POST, instance=instancia_sesion)

        try:
            if form.is_valid():
                sesion_grupal = form.save(commit=False)

                if accion == 'agregar':
                    ultima_sesion = CGrupal.objects.filter(clinica=clinica_actual).aggregate(max_sesion=models.Max('sesion'))['max_sesion']
                    nuevo_numero = (ultima_sesion or 0) + 1
                    sesion_grupal.sesion = nuevo_numero
                    sesion_grupal.clinica = clinica_actual
                    sesion_grupal.consejero=mem_user_no
                    sesion_grupal.nombreconsejero=mem_user_nombre

                    sesion_grupal.status = 0
                    mensaje = f'Sesión grupal #{sesion_grupal.sesion} creada correctamente.'

                else:  # EDITAR
                    if request.POST.get('status') == '1':
                        # 🔥 VALIDACIÓN CORREGIDA - Validar ANTES de cerrar
                        proximasesion_str = request.POST.get('proximasesion')

                        # Validar primero
                        error_validacion = None
                        if not proximasesion_str:
                            error_validacion = 'Error: Debe especificar una fecha para la próxima sesión al cerrar la sesión actual'
                        elif proximasesion_str:
                            from datetime import datetime
                            try:
                                # Convertir de YYYY-MM-DD (formato input) a date
                                proximasesion = datetime.strptime(proximasesion_str, '%Y-%m-%d').date()

                                if proximasesion <= sesion_grupal.fecha:
                                    error_validacion = f'Error: La próxima sesión debe ser posterior a la fecha de esta sesión ({sesion_grupal.fecha.strftime("%d/%m/%Y")})'
                                elif proximasesion < date.today():
                                    error_validacion = 'Error: La próxima sesión no puede ser una fecha pasada'

                            except ValueError:
                                error_validacion = 'Error: Formato de fecha inválido'

                        # Si hay error, NO cerrar la sesión
                        if error_validacion:
                            messages.error(request, error_validacion)
                            participantes_ids = request.POST.getlist('participantes')
                            if participantes_ids:
                                participantes_ids = [int(id) for id in participantes_ids if id.isdigit()]
                                participantes_seleccionados = Internos.objects.filter(id__in=participantes_ids)

                            context = {
                                'tipo_sesion': 'grupal',
                                'accion': accion,
                                'verbose_name': 'Sesión Grupal',
                                'form': form,
                                'instancia_sesion': instancia_sesion,
                                'internos_grupo': internos_disponibles,
                                'participantes_seleccionados': participantes_seleccionados,
                            }
                            return render(request, 'captura_sesion.html', context)

                        # 🔥 SOLO SI NO HAY ERROR, cerrar la sesión
                        sesion_grupal.status = 1
                        mensaje = 'Sesión grupal cerrada correctamente.'

                        sesion_grupal.save()

                        participantes_ids = request.POST.getlist('participantes')
                        if participantes_ids:
                            participantes_ids = [int(id) for id in participantes_ids if id.isdigit()]
                            participantes = Internos.objects.filter(id__in=participantes_ids)
                            sesion_grupal.participantes.set(participantes)
                            sesion_grupal.numero_participantes = participantes.count()
                        else:
                            sesion_grupal.participantes.clear()
                            sesion_grupal.numero_participantes = 0

                        sesion_grupal.save()

                        messages.success(request, mensaje)
                        return redirect('capturaSesionGrupal', tipo_sesion=tipo_sesion, accion='agregar')
                    else:
                        mensaje = 'Sesión grupal actualizada correctamente.'

                # Guardar para sesiones nuevas y ediciones normales
                sesion_grupal.save()

                participantes_ids = request.POST.getlist('participantes')
                if participantes_ids:
                    participantes_ids = [int(id) for id in participantes_ids if id.isdigit()]
                    participantes = Internos.objects.filter(id__in=participantes_ids,clinica=clinica_actual)
                    sesion_grupal.participantes.set(participantes)
                    sesion_grupal.numero_participantes = participantes.count()
                else:
                    sesion_grupal.participantes.clear()
                    sesion_grupal.numero_participantes = 0

                sesion_grupal.save()

                messages.success(request, mensaje)

                if accion == 'agregar':
                    return redirect('listaSesionesGrupales')
                else:
                    return redirect('capturaSesionGrupal_con_id', tipo_sesion=tipo_sesion, accion='editar',
                                    no_sesion=sesion_grupal.pk)

        except Exception as e:
            print(f"🔍 DEBUG - Error: {e}")
            messages.error(request, f'Error al guardar la sesión grupal: {str(e)}')
    else:
        form = CGrupalf(instance=instancia_sesion)

    if accion == 'agregar' and not instancia_sesion:
        ultima_sesion = CGrupal.objects.aggregate(max_sesion=models.Max('sesion'))['max_sesion']
        siguiente_numero = (ultima_sesion or 0) + 1
    else:
        siguiente_numero = None

    context = {
        'tipo_sesion': 'grupal',
        'accion': accion,
        'verbose_name': 'Sesión Grupal',
        'form': form,
        'instancia_sesion': instancia_sesion,
        'internos_grupo': internos_disponibles,
        'participantes_seleccionados': participantes_seleccionados,
        'siguiente_numero': siguiente_numero,
        'id': interno_actual_id,
    }

    return render(request, 'captura_sesion.html', context)

def capturaSesionPS(request, accion, id=None, no_sesion=None):

    clinica_actual=get_clinica_actual(request)
    interno = Internos.objects.get(numeroexpediente=id,clinica=clinica_actual)

    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'PSICOLOGIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    if id is None and 'interno_actual_id' in request.session:
        id = request.session['interno_actual_id']


    modelo = NotasEvolucionPS
    verbose_name = 'Notas de evolucion psicologica'
    form_class = NotasEvolucionPSf

    cuantas_sesiones = 0
    nueva_sesion = 1
    cerrada = True
    ultima_sesion_obj = None
    instancia_sesion = None

    if accion == 'agregar':
        sesiones_existentes = modelo.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).order_by('sesion')
        cuantas_sesiones = sesiones_existentes.count()

        if sesiones_existentes:
            ultima_sesion_obj = sesiones_existentes.last()
            nueva_sesion = ultima_sesion_obj.sesion + 1

            if ultima_sesion_obj.status == 1:
                cerrada = True
            else:
                cerrada = False

            if not cerrada:
                messages.error(request, 'La sesión anterior no está cerrada por lo tanto no puede crear una nueva.')
                return redirect('listaSesionesPS',  id=id)

    if accion == 'editar' and no_sesion is not None:
        try:
            instancia_sesion = modelo.objects.get(pk=no_sesion)
            nueva_sesion = instancia_sesion.sesion
            cerrada = (instancia_sesion.status == 1)
        except modelo.DoesNotExist:
            messages.error(request, f'{verbose_name} a editar no encontrada.')
            return redirect('listaSesionesPS', id=interno.numeroexpediente)
    else:
        instancia_sesion = modelo()

    if request.method == 'POST':
        form = form_class(request.POST, instance=instancia_sesion)
        if form.is_valid():
            sesion_guardar = form.save(commit=False)
            sesion_guardar.expediente = interno.numeroexpediente
            sesion_guardar.clinica = clinica_actual
            if not sesion_guardar.psicologo or sesion_guardar.psicologo==0:
               sesion_guardar.psicologo=mem_user_no
               sesion_guardar.nombrepsicologo=mem_user_nombre


            # 🔥 VALIDACIÓN CORREGIDA - Validar ANTES de cerrar
            if accion == 'editar' and request.POST.get('status') == '1':
                proximasesion_str = request.POST.get('proximasesion')

                # Validar primero
                error_validacion = None
                if not proximasesion_str:
                    error_validacion = 'Error: Debe especificar una fecha para la próxima sesión al cerrar la sesión actual'
                elif proximasesion_str:
                    from datetime import datetime
                    try:
                        # Convertir de YYYY-MM-DD (formato input) a date
                        proximasesion = datetime.strptime(proximasesion_str, '%Y-%m-%d').date()

                        if proximasesion <= sesion_guardar.fecha:
                            error_validacion = f'Error: La próxima sesión debe ser posterior a la fecha de esta sesión ({sesion_guardar.fecha.strftime("%d/%m/%Y")})'
                        elif proximasesion < date.today():
                            error_validacion = 'Error: La próxima sesión no puede ser una fecha pasada'

                    except ValueError:
                        error_validacion = 'Error: Formato de fecha inválido'

                # Si hay error, NO cerrar la sesión
                if error_validacion:
                    messages.error(request, error_validacion)
                    context = {
                        'form': form,
                        'id_expediente': id,
                        'numero_expediente': interno.numeroexpediente,
                        'numero_sesion_actual': nueva_sesion,
                        'verbose_name': verbose_name,
                        'interno': interno,
                        'cuantas_sesiones': cuantas_sesiones,
                        'cerrada': cerrada,
                        'ultima_sesion': ultima_sesion_obj,
                        'accion': accion,
                        'instancia_sesion': instancia_sesion,
                    }
                    return render(request, 'captura_sesionps.html', context)

                # 🔥 SOLO SI NO HAY ERROR, continuar (la sesión se cierra después)

            if accion == 'agregar':
                sesion_guardar.sesion = nueva_sesion

            sesion_guardar.save()
            messages.success(request, f'{verbose_name} {sesion_guardar.sesion} guardada exitosamente.')
            return redirect('listaSesionesPS',  id=id)
        else:
            messages.error(request, 'Error al guardar la sesión. Revisa los campos.')
    else:
        if instancia_sesion:
            form = form_class(instance=instancia_sesion)
        else:
            form = form_class(initial={
                'expediente': interno.numeroexpediente,
                'sesion': nueva_sesion,

            })

    context = {
        'form': form,
        'id_expediente': id,
        'numero_expediente': interno.numeroexpediente,
        'numero_sesion_actual': nueva_sesion,
        'verbose_name': verbose_name,
        'interno': interno,
        'cuantas_sesiones': cuantas_sesiones,
        'cerrada': cerrada,
        'ultima_sesion': ultima_sesion_obj,
        'accion': accion,
        'instancia_sesion': instancia_sesion,
    }

    return render(request, 'captura_sesionps.html', context)


def capturaSesionS(request, accion, id=None, no_sesion=None):

    clinica_actual=get_clinica_actual(request)
    interno = Internos.objects.get(numeroexpediente=id,clinica=clinica_actual)

    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

    if id is None and 'interno_actual_id' in request.session:
        id = request.session['interno_actual_id']


    modelo = NotasSeguimiento
    verbose_name = 'Notas de seguimiento'
    form_class = NotasSeguimientof

    cuantas_sesiones = 0
    nueva_sesion = 1
    cerrada = True
    ultima_sesion_obj = None
    instancia_sesion = None

    if accion == 'agregar':
        sesiones_existentes = modelo.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).order_by('sesion')
        cuantas_sesiones = sesiones_existentes.count()

        if sesiones_existentes:
            ultima_sesion_obj = sesiones_existentes.last()
            nueva_sesion = ultima_sesion_obj.sesion + 1

            if ultima_sesion_obj.status == 1:
                cerrada = True
            else:
                cerrada = False

            if not cerrada:
                messages.error(request, 'La sesión anterior no está cerrada por lo tanto no puede crear una nueva.')
                return redirect('listaSesionesS',  id=id)

    if accion == 'editar' and no_sesion is not None:
        try:
            instancia_sesion = modelo.objects.get(pk=no_sesion)
            nueva_sesion = instancia_sesion.sesion
            cerrada = (instancia_sesion.status == 1)
        except modelo.DoesNotExist:
            messages.error(request, f'{verbose_name} a editar no encontrada.')
            return redirect('listaSesionesS', id=interno.numeroexpediente)
    else:
        instancia_sesion = None

    if request.method == 'POST':
        form = form_class(request.POST, instance=instancia_sesion)
        if form.is_valid():
            sesion_guardar = form.save(commit=False)
            sesion_guardar.expediente = interno.numeroexpediente
            sesion_guardar.consejero = mem_user_no
            sesion_guardar.nombreconsejero = mem_user_nombre
            sesion_guardar.clinica = clinica_actual

            # 🔥 VALIDACIÓN CORREGIDA - Validar ANTES de cerrar
            if accion == 'editar' and request.POST.get('status') == '1':
                proximasesion_str = request.POST.get('proximasesion')

                # Validar primero
                error_validacion = None
                if not proximasesion_str:
                    error_validacion = 'Error: Debe especificar una fecha para la próxima sesión al cerrar la sesión actual'
                elif proximasesion_str:
                    from datetime import datetime
                    try:
                        # Convertir de YYYY-MM-DD (formato input) a date
                        proximasesion = datetime.strptime(proximasesion_str, '%Y-%m-%d').date()

                        if proximasesion <= sesion_guardar.fecha:
                            error_validacion = f'Error: La próxima sesión debe ser posterior a la fecha de esta sesión ({sesion_guardar.fecha.strftime("%d/%m/%Y")})'
                        elif proximasesion < date.today():
                            error_validacion = 'Error: La próxima sesión no puede ser una fecha pasada'

                    except ValueError:
                        error_validacion = 'Error: Formato de fecha inválido'

                # Si hay error, NO cerrar la sesión
                if error_validacion:
                    messages.error(request, error_validacion)
                    context = {
                        'form': form,
                        'id_expediente': id,
                        'numero_expediente': interno.numeroexpediente,
                        'numero_sesion_actual': nueva_sesion,
                        'verbose_name': verbose_name,
                        'interno': interno,
                        'cuantas_sesiones': cuantas_sesiones,
                        'cerrada': cerrada,
                        'ultima_sesion': ultima_sesion_obj,
                        'accion': accion,
                        'instancia_sesion': instancia_sesion,
                    }
                    return render(request, 'captura_sesions.html', context)

                # 🔥 SOLO SI NO HAY ERROR, continuar (la sesión se cierra después)

            if accion == 'agregar':
                sesion_guardar.sesion = nueva_sesion

            sesion_guardar.save()
            messages.success(request, f'{verbose_name} {sesion_guardar.sesion} guardada exitosamente.')
            return redirect('listaSesionesS',  id=id)
        else:
            messages.error(request, 'Error al guardar la sesión. Revisa los campos.')
    else:
        if instancia_sesion:
            form = form_class(instance=instancia_sesion)
        else:
            form = form_class(initial={
                'expediente': interno.numeroexpediente,
                'sesion': nueva_sesion,

            })

    context = {
        'form': form,
        'id_expediente': id,
        'numero_expediente': interno.numeroexpediente,
        'numero_sesion_actual': nueva_sesion,
        'verbose_name': verbose_name,
        'interno': interno,
        'cuantas_sesiones': cuantas_sesiones,
        'cerrada': cerrada,
        'ultima_sesion': ultima_sesion_obj,
        'accion': accion,
        'instancia_sesion': instancia_sesion,
    }

    return render(request, 'captura_sesions.html', context)





def listaSesionesGrupales(request,id=None):
    """
    Vista para listar todas las sesiones grupales
    """
    clinica_actual = get_clinica_actual(request)
    sesiones_grupales = CGrupal.objects.filter(clinica=clinica_actual).order_by('-fecha', '-sesion')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    interno = None
    if id:
        try:
            interno = Internos.objects.get(numeroexpediente=id,clinica=clinica_actual)
        except Internos.DoesNotExist:
            pass
    context = {
        'sesiones_grupales': sesiones_grupales,
        'id':id,
        'interno': interno,

    }
    return render(request, 'lista_sesiones_grupales.html', context)


def listaSesionesPS(request,id=None):
    """
    Vista para listar todas las sesiones grupales
    """
    clinica_actual=get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'PSICOLOGIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    interno=Internos.objects.get(numeroexpediente=id,clinica=clinica_actual)
    clinica_actual=get_clinica_actual(request)

    sesionesPS = NotasEvolucionPS.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).order_by('-fecha', '-sesion')

    interno = None
    if id:
        try:
            interno = Internos.objects.get(numeroexpediente=id,clinica=clinica_actual)
        except Internos.DoesNotExist:
            pass
    context = {
        'sesionesPS': sesionesPS,
        'id':id,
        'interno': interno,

    }
    return render(request, 'lista_notasevolucionps.html', context)

def listaSesionesS(request,id=None):
    """
    Vista para listar todas las sesiones grupales
    """
    clinica_actual=get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    interno=Internos.objects.get(numeroexpediente=id,clinica=clinica_actual)
    clinica_actual=get_clinica_actual(request)

    sesiones = NotasSeguimiento.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).order_by('-fecha', '-sesion')

    interno = None
    if id:
        try:
            interno = Internos.objects.get(numeroexpediente=id,clinica=clinica_actual)
        except Internos.DoesNotExist:
            pass
    context = {
        'sesiones': sesiones,
        'id':id,
        'interno': interno,

    }
    return render(request, 'lista_notasseguimiento.html', context)


def planConsejeria(request, id):
    """
    Obtiene el interno por ID y luego busca/crea su consejería
    """
    # 1. Obtener el interno
    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    # 2. Buscar consejería existente o crear una nueva
    try:
        # Primero intentar obtener una existente
        pconsejeria = PConsejeria.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False
        print(f"=== DEBUG: Plan existente encontrado - ID: {pconsejeria.id} ===")
        print(f"=== DEBUG: con expediente : {pconsejeria.expediente} ===")
    except PConsejeria.DoesNotExist:
        # Si no existe, crear una nueva
        pconsejeria = PConsejeria(expediente=interno.numeroexpediente)
        pconsejeria.consejero = mem_user_no
        pconsejeria.nombreconsejero = mem_user_nombre
        pconsejeria.clinica = clinica_actual
        pconsejeria.save()
        creado = True
        print(f"=== DEBUG: Nuevo plan creado - ID: {pconsejeria.id} ===")
        print(f"=== DEBUG: con expediente : {pconsejeria.expediente} ===")
    except PConsejeria.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        pconsejeria = PConsejeria.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).latest('id')
        creado = False
        print(f"=== DEBUG: Múltiples planes, tomando el más reciente - ID: {pconsejeria.id} ===")

    if request.method == 'POST':
        print("=== DEBUG: POST recibido ===")
        print(f"=== DEBUG: Datos POST: {request.POST} ===")  # Ver qué datos llegan

        # Crear el formulario con los datos del POST y la instancia existente
        pconsejeriaf = PConsejeriaf(request.POST, instance=pconsejeria)

        print(f"Formulario válido: {pconsejeriaf.is_valid()}")

        if pconsejeriaf.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = pconsejeriaf.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente  # Asegurar el expediente
            saved_instance.clinica = clinica_actual
            saved_instance.save()

            print(f"=== DEBUG: Guardado exitoso - ID: {saved_instance.id} ===")
            print(f"=== DEBUG: Expediente guardado: {saved_instance.expediente} ===")
            messages.success(request, 'Plan de consejería guardado exitosamente.')

            # Recargar el formulario con los datos guardados
            pconsejeriaf = PConsejeriaf(instance=saved_instance)
        else:
            print(f"=== DEBUG: Errores del formulario: {pconsejeriaf.errors} ===")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # GET request - mostrar formulario con datos existentes
        pconsejeriaf = PConsejeriaf(instance=pconsejeria)
        print(f"=== DEBUG: GET - Instancia: {pconsejeria.id}, Creado: {creado} ===")

    return render(request, 'plan_consejeria.html', {
        'pconsejeria': pconsejeria,
        'interno': interno,
        'pconsejeriaf': pconsejeriaf,
        'creado': creado,
    })


import requests


def escanear_tarea(request):
    expediente = request.session.get('expediente_actual')
    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    if not expediente:
        messages.error(request, 'No hay expediente en sesión')
        return redirect('listaint')

    interno = get_object_or_404(Internos, numeroexpediente=expediente, clinica=clinica_actual)
    modelo = TareaConsejeria
    form_class = TareaConsejeriaf

    cuantas_tareas = 0
    nueva_tarea = 1
    ultima_sesion_obj = None
    instancia_sesion = None

    tareas_existentes = modelo.objects.filter(expediente=interno.numeroexpediente,
                                                    clinica=clinica_actual).order_by('numero_tarea')
    cuantas_tareas = tareas_existentes.count()

    if tareas_existentes:
       ultima_tarea_obj = tareas_existentes.last()
       nueva_tarea = ultima_tarea_obj.numero_tarea + 1

    if request.method == 'POST':
        # DEBUG: Ver qué llega en el request
        print(f"📨 POST keys: {list(request.POST.keys())}")
        print(f"📁 FILES keys: {list(request.FILES.keys())}")

        form = TareaConsejeriaf(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.expediente = expediente
            instance.clinica = clinica_actual
            instance.numero_tarea = nueva_tarea

            # DEBUG: Verificar el campo específico
            print(f"🔍 Buscando 'imagen_tarea' en FILES: {'imagen_tarea' in request.FILES}")

            if 'imagen_tarea' in request.FILES and request.FILES['imagen_tarea']:
                print("🔄 EJECUTANDO ImgBB upload...")
                try:
                    api_key = '8c061775423c7c7ffc99af2f3ed63c42'
                    files = {'image': request.FILES['imagen_tarea']}

                    response = requests.post(
                        f"https://api.imgbb.com/1/upload?key={api_key}",
                        files=files
                    )
                    print(f"📡 Status Code ImgBB: {response.status_code}")

                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ URL ImgBB: {result['data']['url']}")
                        instance.imagen_tarea_url = result['data']['url']
                    else:
                        print(f"❌ Error ImgBB: {response.text}")

                except Exception as e:
                    print(f"💥 Excepción: {e}")
            else:
                print("❌ No se encontró imagen_tarea en FILES")

            instance.save()
            messages.success(request, 'Tarea escaneada y guardada exitosamente')
            return redirect('escanear_tarea')
        else:
            print(f"❌ Formulario inválido: {form.errors}")

    else:
        form = TareaConsejeriaf()

    return render(request, 'escanear_tarea.html', {
        'form': form,
        'expediente': expediente,
        'interno': interno,
    })



def lista_tareas_escaneadas(request):
    # Obtener expediente de la sesión
    expediente = request.session.get('expediente_actual')
    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')


    if not expediente:
        messages.error(request, 'No hay expediente en sesión')
        return redirect('listaint')

    interno = get_object_or_404(Internos, numeroexpediente=expediente,clinica=clinica_actual)
    # Obtener todas las tareas del expediente
    tareas = TareaConsejeria.objects.filter(expediente=expediente,clinica=clinica_actual).order_by('-fecha_creacion')

    return render(request, 'lista_tareas.html', {
        'tareas': tareas,
        'expediente': expediente,
        'interno':interno,
    })


def eliminar_tarea(request, tarea_id):

    clinica_actual= get_clinica_actual(request)
    tarea = get_object_or_404(TareaConsejeria, pk=tarea_id,clinica=clinica_actual)
    expediente = tarea.expediente

    tarea.delete()
    messages.success(request, 'Tarea eliminada exitosamente')
    return redirect('lista_tareas_escaneadas')




def lista_archivos_word(request):
    # Ruta base de documentos Word
    carpeta_base = '\Prgadicciones\ctrlinfo\mapp\media\Tareas'


    print(f'carpeta base {carpeta_base}')
    # Crear carpeta base si no existe
    os.makedirs(carpeta_base, exist_ok=True)

    # Estructura para organizar archivos por carpeta
    estructura = {
        'carpetas': [],
        'total_archivos': 0
    }

    # Recorrer todas las subcarpetas
    for nombre_carpeta in os.listdir(carpeta_base):
        ruta_carpeta = os.path.join(carpeta_base, nombre_carpeta)
        print(f'ruta_carpeta')
        if os.path.isdir(ruta_carpeta):
            # Buscar archivos Word en esta subcarpeta
            archivos_carpeta = []

            for archivo in os.listdir(ruta_carpeta):
                if archivo.lower().endswith(('.doc', '.docx')):
                    ruta_completa = os.path.join(ruta_carpeta, archivo)
                    archivos_carpeta.append({
                        'nombre': archivo,
                        'ruta_completa': ruta_completa,
                        'ruta_relativa': f"{nombre_carpeta}/{archivo}",
                        'tamaño': os.path.getsize(ruta_completa),
                        'fecha_modificacion': os.path.getmtime(ruta_completa)
                    })

            # Si la carpeta tiene archivos Word, agregarla a la estructura
            if archivos_carpeta:
                # Ordenar archivos por nombre
                archivos_carpeta.sort(key=lambda x: x['nombre'])

                estructura['carpetas'].append({
                    'nombre': nombre_carpeta,
                    'archivos': archivos_carpeta,
                    'cantidad_archivos': len(archivos_carpeta)
                })

                estructura['total_archivos'] += len(archivos_carpeta)

    # Ordenar carpetas por nombre
    estructura['carpetas'].sort(key=lambda x: x['nombre'])

    return render(request, 'imprimir_tareas.html', {
        'estructura': estructura
    })


def imprimir_archivos_word(request):
    if request.method == 'POST':
        archivos_seleccionados = request.POST.getlist('archivos[]')
        carpeta_base = os.path.join(settings.MEDIA_ROOT, 'Tareas')

        resultados = []

        try:
            # Inicializar COM
            pythoncom.CoInitialize()

            # Crear instancia de Word
            word_app = win32com.client.Dispatch("Word.Application")
            word_app.Visible = False

            for ruta_relativa in archivos_seleccionados:
                try:
                    # La ruta_relativa viene como "carpeta/archivo.docx"
                    ruta_completa = os.path.join(carpeta_base, ruta_relativa)

                    if os.path.exists(ruta_completa):
                        # Abrir documento
                        doc = word_app.Documents.Open(ruta_completa)

                        # Imprimir documento
                        doc.PrintOut()

                        # Cerrar documento
                        doc.Close(SaveChanges=False)

                        resultados.append({
                            'archivo': ruta_relativa,
                            'estado': '✅ Enviado a impresión',
                            'error': None
                        })
                    else:
                        resultados.append({
                            'archivo': ruta_relativa,
                            'estado': '❌ No encontrado',
                            'error': 'Archivo no existe'
                        })

                except Exception as e:
                    resultados.append({
                        'archivo': ruta_relativa,
                        'estado': '❌ Error',
                        'error': str(e)
                    })

            # Cerrar Word
            word_app.Quit()

            return JsonResponse({
                'success': True,
                'resultados': resultados,
                'mensaje': f'Procesados {len(archivos_seleccionados)} archivos'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error general: {str(e)}'
            })

        finally:
            # Asegurar que COM se libera
            pythoncom.CoUninitialize()

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def hojaAtencionPs(request, id):
    """
    Obtiene el interno por ID y luego busca/crea su consejería
    """
    # 1. Obtener el interno

    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'PSICOLOGIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, numeroexpediente=id,clinica=clinica_actual)

    # 2. Buscar consejería existente o crear una nueva
    try:
        hatencionps = HojaAtencionPs.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
        creado = False

    except HojaAtencionPs.DoesNotExist:
        # Si no existe, crear una nueva
        hatencionps = HojaAtencionPs(expediente=interno.numeroexpediente)
        hatencionps.psicologo=mem_user_no
        hatencionps.nombrepsicologo=mem_user_nombre
        hatencionps.clinica=clinica_actual
        hatencionps.save()
        creado = True
        print(f"=== DEBUG: Nuevo plan creado - ID: {hatencionps.id} ===")
        print(f"=== DEBUG: con expediente : {hatencionps.expediente} ===")
    except HojaAtencionPs.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        hatencionps = HojaAtencionPs.objects.filter(expediente=interno.numeroexpediente).latest('id')
        creado = False
        print(f"=== DEBUG: Múltiples planes, tomando el más reciente - ID: {hatencionps.id} ===")

    if request.method == 'POST':
        # Crear el formulario con los datos del POST y la instancia existente
        hatencionpsf = HojaAtencionPsf(request.POST, instance=hatencionps)

        print(f"Formulario válido: {hatencionpsf.is_valid()}")

        if hatencionpsf.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = hatencionpsf.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente
            saved_instance.clinica=clinica_actual# Asegurar el expediente
            if not saved_instance.psicologo or saved_instance.psicologo==0:
               saved_instance.psicologo=mem_user_no # Asegurar el expediente
               saved_instance.nombrepsicologo=mem_user_nombre

            saved_instance.save()

            messages.success(request, 'Hoja de atencion psicologica guardada exitosamente.')

            # Recargar el formulario con los datos guardados
            hatencionpsf = HojaAtencionPsf(instance=saved_instance)
        else:
            print(f"=== DEBUG: Errores del formulario: {hatencionpsf.errors} ===")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # GET request - mostrar formulario con datos existentes
        hatencionpsf = HojaAtencionPsf(instance=hatencionps)
        print(f"=== DEBUG: GET - Instancia: {hatencionps.id}, Creado: {creado} ===")

    return render(request, 'hoja_atencionps.html', {
        'hatencionps': hatencionps,
        'interno': interno,
        'hatencionpsf': hatencionpsf,
        'creado': creado,
    })



def medicoInicial(request, id):
    """
    Obtiene el interno por ID y luego busca/crea su consejería
    """
    # 1. Obtener el interno
    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'MEDICO' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    # 2. Buscar consejería existente o crear una nueva
    try:
        # Primero intentar obtener una existente
        medicoinicial = Medico.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False

    except Medico.DoesNotExist:
        # Si no existe, crear una nueva
        medicoinicial = Medico(expediente=interno.numeroexpediente)
        medicoinicial.medico = mem_user_no
        medicoinicial.nombremedico = mem_user_nombre
        medicoinicial.clinica = clinica_actual

        medicoinicial.save()
        creado = True
    except Medico.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        medicoinicial = Medico.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).latest('id')
        creado = False
        print(f"=== DEBUG: Múltiples planes, tomando el más reciente - ID: {medicoinicial.id} ===")

    if request.method == 'POST':


        # Crear el formulario con los datos del POST y la instancia existente
        medicof = Medicof(request.POST, instance=medicoinicial)

        if medicof.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = medicof.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente  # Asegurar el expediente
            saved_instance.clinica = clinica_actual  # Asegurar el expediente


            saved_instance.save()

            messages.success(request, 'Examen medico inicial guardado exitosamente.')

            # Recargar el formulario con los datos guardados
            medicof = Medicof(instance=saved_instance)
        else:
            print(f"=== DEBUG: Errores del formulario: {medicof.errors} ===")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # GET request - mostrar formulario con datos existentes
        medicof = Medicof(instance=medicoinicial)
        print(f"=== DEBUG: GET - Instancia: {medicoinicial.id}, Creado: {creado} ===")

    return render(request, 'medico_inicial.html', {
        'medicoinicial': medicoinicial,
        'interno': interno,
        'medicof': medicof,
        'creado': creado,
    })

def emisionDerecetas(request,id):


    clinica_actual=get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'MEDICO' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')


    try:
        # Primero intentar obtener una existente
        receta = Recetas.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False


    except Recetas.DoesNotExist:
        # Si no existe, crear una nueva
        receta = Recetas(expediente=interno.numeroexpediente)
        receta.clinica = clinica_actual
        receta.medico = mem_user_no
        receta.nombremedico = mem_user_nombre

        receta.save()
        creado = True
        print(f"=== DEBUG: Nuevo plan creado - ID: {receta.id} ===")
        print(f"=== DEBUG: con expediente : {receta.expediente} ===")

    except Recetas.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        receta = Recetas.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).latest('id')
        creado = False

    if request.method == 'POST':
        # Crear el formulario con los datos del POST y la instancia existente
        recetaf = Recetasf(request.POST, instance=receta)

        print(f"Formulario válido: {recetaf.is_valid()}")

        if recetaf.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = recetaf.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente  # Asegurar el expediente
            saved_instance.clinica = clinica_actual  # Asegurar el expediente
            if not saved_instance.medico or saved_instance.medico==0:
                saved_instance.medico=mem_user_no
                saved_instance.nombremedico=mem_user_nombre

            saved_instance.save()

            print(f"=== DEBUG: Guardado exitoso - ID: {saved_instance.id} ===")
            print(f"=== DEBUG: Expediente guardado: {saved_instance.expediente} ===")
            messages.success(request, 'Receta  guardada exitosamente.')

            # Recargar el formulario con los datos guardados
            recetaf = Recetasf(instance=saved_instance)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # GET request - mostrar formulario con datos existentes
        recetaf = Recetasf(instance=receta)
        print(f"=== DEBUG: GET - Instancia: {receta.id}, Creado: {creado} ===")

    return render(request, 'emision_recetas.html', {
        'receta': receta,
        'interno': interno,
        'recetaf': recetaf,
        'id': id,
    })

def historiaClinica(request, id):
    """
    Obtiene el interno por ID y luego busca/crea su consejería
    """
    # 1. Obtener el interno
    clinica_actual=get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'MEDICO' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

      # 2. Buscar consejería existente o crear una nueva
    try:
        # Primero intentar obtener una existente
        historiaclinica = HistoriaClinica.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False

    except HistoriaClinica.DoesNotExist:
        # Si no existe, crear una nueva
        historiaclinica = HistoriaClinica(expediente=interno.numeroexpediente)
        historiaclinica.medico = mem_user_no
        historiaclinica.nombremedico = mem_user_nombre
        historiaclinica.clinica = clinica_actual
        historiaclinica.save()
        creado = True

    except HistoriaClinica.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        historiaclinica = HistoriaClinica.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).latest('id')
        creado = False
        print(f"=== DEBUG: Múltiples planes, tomando el más reciente - ID: {historiaclinica.id} ===")

    if request.method == 'POST':


        historiaclinica.clinica=clinica_actual

        # Crear el formulario con los datos del POST y la instancia existente
        historiaclinicaf = HistoriaClinicaf(request.POST, instance=historiaclinica)

        print(f"Formulario válido: {historiaclinicaf.is_valid()}")

        if historiaclinicaf.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = historiaclinicaf.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente  # Asegurar el expediente

            saved_instance.clinica = clinica_actual  # Asegurar el expediente

            # Asegurar que el médico sea el usuario actual - CORREGIDO
            if not saved_instance.medico:
                saved_instance.medico = mem_user_no
                saved_instance.clinica = clinica_actual

            saved_instance.save()

            messages.success(request, 'Examen medico inicial guardado exitosamente.')

            # Recargar el formulario con los datos guardados
            historiaclinicaf = HistoriaClinicaf(instance=saved_instance)
        else:
            print(f"=== DEBUG: Errores del formulario: {historiaclinicaf.errors} ===")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # GET request - mostrar formulario con datos existentes
        historiaclinicaf = HistoriaClinicaf(instance=historiaclinica)
        print(f"=== DEBUG: GET - Instancia: {historiaclinica.id}, Creado: {creado} ===")

    sistemas_fields = [
        ('digestivo', 'Digestivo'),
        ('cardiovascular', 'Cardiovascular'),
        ('respiratorio', 'Respiratorio'),
        ('urinario', 'Urinario'),
        ('genital', 'Genital'),
        ('hematologico', 'Hematológico'),
        ('endocrino', 'Endocrino'),
        ('osteomuscular', 'Osteomuscular'),
        ('nervioso', 'Nervioso'),
        ('sensorial', 'Sensorial'),
        ('psicomatico', 'Psicosomático'),
    ]
    return render(request, 'historia_clinica.html', {
        'historiaclinica': historiaclinica,
        'interno': interno,
        'historiaclinicaf': historiaclinicaf,
        'sistemas_fields': sistemas_fields,
        'mem_user_no' : mem_user_no,
        'mem_user_nombre': mem_user_nombre,


    })




@csrf_exempt
def validar_usuario(request):
    if request.method == 'POST':
        usuario_numero = request.POST.get('usuario')
        password = request.POST.get('password')

        try:
            # Buscar usuario por número
            usuario = Usuarios.objects.get(usuario=usuario_numero,
                      clinica=request.session.get('clinica_actual', 'Demostracion'))

            # Verificar password
            if usuario.password == password:

                request.session['usuario_autenticado'] = True
                request.session['usuario_id'] = usuario.id
                request.session['usuario_no'] = usuario.usuario
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_cargo'] = usuario.cargo
                request.session['usuario_permisos'] = usuario.permisos


                return JsonResponse({
                    'success': True,
                    'nombre': usuario.nombre,
                    'cargo': usuario.cargo,
                    'permisos': usuario.permisos
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Contraseña incorrecta'
                })

        except Usuarios.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            })

    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })


@csrf_exempt
def cerrar_sesion(request):
    if request.method == 'POST':
        # Limpiar toda la sesión
        keys_to_delete = [
            'usuario_autenticado',
            'usuario_id',
            'usuario_no',
            'usuario_nombre',
            'usuario_cargo',
            'usuario_permisos'
        ]

        for key in keys_to_delete:
            if key in request.session:
                del request.session[key]

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


# views.py - ACTUALIZA tu vista de login
def login_clinica(request):
    if request.method == 'POST':
        form = ClinicaLoginForm(request.POST)
        if form.is_valid():
            clinica_id = form.cleaned_data['clinica_id']
            password = form.cleaned_data['password']
           # clinica_id=''
           # password=''
           # request.session['clinica_actual'] = 'Demostracion'
           # request.session['clinica_nombre'] = 'Centro de Rehabilitacion VIVE, A.C.'
           # return redirect('dashboard')
            try:
                clinica = Clinicas.objects.get(clinica=clinica_id)
                if clinica.password == password:  # Verificación simple
                    # GUARDAR en sesión
                    request.session['clinica_actual'] = clinica.clinica
                    request.session['clinica_nombre'] = clinica.nombre
                    request.session['ffazzuorrtt'] = clinica.password

                    return redirect('dashboard')
                else:
                    form.add_error('password', 'Contraseña incorrecta')
            except Clinicas.DoesNotExist:
                form.add_error('clinica_id', 'Clínica no encontrada')
    else:
        form = ClinicaLoginForm()

    return render(request, 'login.html', {'form': form})



def dashboard(request):
    # 1. Seguridad: Si no han entrado a la clínica, mandar al login
    if 'clinica_actual' not in request.session:
        return redirect('login_clinica')

    # 2. Obtener el ID de la clínica de la sesión
    clinica_nombre = request.session.get('clinica_actual')

    # 3. Buscar los usuarios de ESTA clínica para llenar el Modal
    # Agregué .order_by('nombre') para que salgan en orden alfabético
    usuarios_lista = Usuarios.objects.filter(clinica=clinica_nombre).order_by('nombre')

    # 4. Empaquetar los datos
    context = {
        'usuarios_para_login': usuarios_lista
    }

    # 5. Renderizar
    return render(request, 'MenuPrincipal.html', context)

def seguimiento(request, id):
    """
    Obtiene el interno por ID y luego busca/crea su consejería
    """
    # 1. Obtener el interno
    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'CONSEJERIA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    # 2. Buscar consejería existente o crear una nueva
    try:
        # Primero intentar obtener una existente
        seguimiento = Seguimiento.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False

    except Seguimiento.DoesNotExist:
        # Si no existe, crear una nueva
        seguimiento = Seguimiento(expediente=interno.numeroexpediente)
        seguimiento.consejero = mem_user_no
        seguimiento.nombreconsejero = mem_user_nombre
        seguimiento.clinica = clinica_actual

        seguimiento.save()
        creado = True
    except Seguimiento.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        seguimiento = Seguimiento.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).latest('id')
        creado = False

    if request.method == 'POST':
        # Crear el formulario con los datos del POST y la instancia existente
        seguimientof = Seguimientof(request.POST, instance=seguimiento)


        if seguimientof.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = seguimientof.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente  # Asegurar el expediente
            saved_instance.clinica = clinica_actual  # Asegurar el expediente


            saved_instance.save()

            messages.success(request, 'Entrevista de seguimiento guardada exitosamente.')

            # Recargar el formulario con los datos guardados
            seguimientof = Seguimientof(instance=saved_instance)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # GET request - mostrar formulario con datos existentes
        seguimientof = Seguimientof(instance=seguimiento)
    form=seguimientof
    return render(request, 'seguimiento.html', {
        'seguimiento': seguimiento,
        'interno': interno,
        'form': form,
        'creado': creado,
    })



import locale
from django.utils import timezone

def reporte_internos(request):
    # Configuración inicial
    form = ReporteFechaForm(request.POST or None)
    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'OFICINA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    datosgrales = DatosGrales.objects.get(clinica=clinica_actual)

    context = {}

    # Intentar poner la fecha en español para el reporte (ej. "8 de Diciembre")
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        pass  # Si falla (común en windows), usará inglés o default

    if request.method == 'POST' and form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']

        # Filtramos los objetos Interno usando el rango de fechas
        # Asumiendo que el campo en tu modelo se llama 'fecha'
        internos = Internos.objects.filter(fechaingreso__range=[fecha_inicio, fecha_fin]).order_by('fechaingreso')

        # Datos para el template
        context = {
            'mostrar_reporte': True,
            'internos': internos,
            'total_ingresos': internos.count(),
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'hoy': timezone.now(),
            'datosgrales':datosgrales,
        }

    context['form'] = form
    return render(request, 'reporte_internos.html', context)


def captura_pagos(request, interno_id=None):
    # 1. Obtener lista para el select
    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'OFICINA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')
    recibo_id_imprimir = request.session.pop('recibo_id_imprimir', None)


    pacientes_lista = Internos.objects.filter(clinica=clinica_actual).order_by('nombrecompleto')

    interno_seleccionado = None
    movimientos = []

    # 2. Si hay búsqueda por GET (del select)
    q_expediente = request.GET.get('q_expediente')

    if q_expediente:
        interno_seleccionado = get_object_or_404(Internos, pk=q_expediente,clinica=clinica_actual)
        # Obtener historial
        movimientos = Edocuenta.objects.filter(expediente=interno_seleccionado.numeroexpediente,clinica=clinica_actual).order_by('fecha')

    # Si viene por URL directa (opcional)
    elif interno_id:
        interno_seleccionado = get_object_or_404(Internos, pk=interno_id,clinica=clinica_actual)
        movimientos = Edocuenta.objects.filter(expediente=interno_seleccionado.numeroexpediente,clinica=clinica_actual).order_by('fecha')

    lista_conceptos = Edocuenta._meta.get_field('concepto').choices
    context = {
        'pacientes_lista': pacientes_lista,
        'interno_seleccionado': interno_seleccionado,
        'movimientos': movimientos,
        'lista_conceptos':lista_conceptos,
        'recibo_id_imprimir': recibo_id_imprimir
    }
    return render(request, 'captura_cuotas.html', context)


from django.db.models import Max
def guardar_pago(request, id):
    # 1. Seguridad: Solo aceptamos POST
    if request.method != 'POST':
        return redirect('captura_pagos')

    clinica_actual = get_clinica_actual(request)
    # 2. Obtener el interno (paciente)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)

    try:
        with transaction.atomic():
            # A. Obtener datos del formulario
            importe_str = request.POST.get('importe')
            recibido_de = request.POST.get('recibido_de')
            fecha_pago = request.POST.get('fecha_pago')
            observaciones = request.POST.get('observaciones', '')
            try:
                mconcepto = int(request.POST.get('concepto', 0))
            except (ValueError, TypeError):
                mconcepto = 0

            p_inicio_str = request.POST.get('periodo_inicio') or None
            p_fin_str = request.POST.get('periodo_fin') or None


            # B. Validaciones
            try:
                monto = float(importe_str)
                if monto <= 0:
                    raise ValueError("El monto debe ser mayor a cero.")
            except (ValueError, TypeError):
                messages.error(request, "El importe ingresado no es válido.")
                # Redirigir de vuelta al paciente seleccionado
                url = reverse('captura_pagos') + f'?q_expediente={id}'
                return redirect(url)

            if mconcepto == 4:
                mtipo='C'
                concepto_detalle = f"Cancelacion de movimiento "
            else:
                mtipo='A'
                concepto_detalle = f"RECIBIMOS DE: {recibido_de}"
                if p_inicio_str and p_fin_str:
                   concepto_detalle += f" CUOTA DEL {p_inicio_str} AL {p_fin_str}"
                elif p_inicio_str:
                   concepto_detalle += f" A PARTIR DEL {p_inicio_str}"

                # ==========================================================
                # NUEVO: CREACIÓN DEL RECIBO (Solo si NO es cancelación)
                # ==========================================================
            recibo_nuevo = None

            if mtipo != 'C':  # Si es un Abono real

                # A. Calcular el siguiente Folio para ESTA clínica
                # Buscamos el número más alto en esta clínica y le sumamos 1
                max_folio = Recibos.objects.filter(clinica=clinica_actual).aggregate(Max('recibo'))['recibo__max']
                nuevo_folio = (max_folio or 0) + 1

                # B. Crear el registro en Recibos
                recibo_nuevo = Recibos.objects.create(
                    recibo=nuevo_folio,
                    expediente=interno.numeroexpediente,  # Guardamos el string, no el objeto
                    fecha=fecha_pago,
                    referencia=concepto_detalle.upper(),
                    importe=monto,
                    operador=mem_user_no,  # ID del usuario logueado
                    nombreoperador=mem_user_nombre,  # Nombre para mostrar
                    clinica=clinica_actual,
                    periodo_inicio=p_inicio_str,
                    periodo_fin=p_fin_str

                )

                # C. Guardar ID en sesión para imprimir ESTE recibo
                request.session['recibo_id_imprimir'] = recibo_nuevo.id




            # D. Crear el Movimiento en Estado de Cuenta (ABONO)
            Edocuenta.objects.create(
                expediente=interno.numeroexpediente,  # Enlace lógico
                fecha=fecha_pago,
                tipo=mtipo,
                concepto=mconcepto,
                referencia=f"{concepto_detalle.upper()} {observaciones.upper()} Recibo #"+str(nuevo_folio),
                importe=monto
            )

            # E. Actualizar el Saldo Maestro del Interno
            # Si el saldo representa DEUDA, un pago la disminuye.
            saldo_actual = float(interno.saldo)
            if mconcepto == 4:
                nuevo_saldo = saldo_actual + monto
            else:
                nuevo_saldo = saldo_actual - monto

            interno.saldo = nuevo_saldo
            interno.save()

            messages.success(request, f"Importe de ${monto:,.2f} aplicado correctamente.")

    except Exception as e:
        messages.error(request, f"Error al guardar el movimiento: {str(e)}")

    # 3. Redirección Inteligente
    # Construimos la URL para volver a la misma pantalla PERO con el paciente seleccionado
    request.session['recibo_id_imprimir'] = recibo_nuevo.id
    messages.success(request, f"Pago aplicado. Generado Recibo #{nuevo_folio if recibo_nuevo else 'N/A'}")
    base_url = reverse('captura_pagos')  # Asegúrate que este sea el 'name' de tu vista principal en urls.py
    return redirect(f"{base_url}?q_expediente={id}")





def cantidad_con_letra(importe):
    """Convierte un número a formato de moneda en letra (Pesos Mexicanos)"""
    enteros = int(importe)
    centavos = int(round((importe - enteros) * 100))

    texto = num2words(enteros, lang='es').upper()

    # Manejo especial para "UN" vs "UNO"
    if enteros == 1:
        texto = "UN"

    return f"{texto} PESOS {centavos:02d}/100 M.N."


def dibujar_recibo(c, y_inicio, datos):
    """
    Dibuja un solo recibo comenzando en la coordenada Y especificada.
    """
    # --- CONFIGURACIÓN DE COLORES Y FUENTES ---
    color_fondo = colors.HexColor("#D1E7D1")
    color_borde = colors.black
    margen_izq = 30
    ancho_util = 550

    # ---------------------------------------------------------
    # 1. ENCABEZADO (LOGO Y RFC)
    # ---------------------------------------------------------
    c.setFillColor(color_fondo)
    c.setStrokeColor(color_borde)
    c.roundRect(margen_izq, y_inicio - 80, 400, 80, 5, fill=1, stroke=1)

    # LOGO (Texto Simulado)
    # --- LÓGICA DEL LOGO (IGUAL QUE TU HTML) ---

    if datos.get('logo_objeto'):
        try:
            # ✅ CORRECTO: Pasamos la variable que contiene el ImageReader
            c.drawImage(datos['logo_objeto'], margen_izq + 10, y_inicio - 75, width=80, height=70, mask='auto',
                        preserveAspectRatio=True)
        except Exception as e:
            print(f"Error pintando logo: {e}")
            # Fallback a texto
            c.setFillColor(colors.green)
            c.setFont("Helvetica-Bold", 35)
            c.drawString(margen_izq + 20, y_inicio - 50, "CLINICA")

    else:
        # Si 'logo_objeto' es None (no se descargó o no existe)
        c.setFillColor(colors.green)
        c.setFont("Helvetica-Bold", 35)
        c.drawString(margen_izq + 20, y_inicio - 50, "CLINICA")
    # 1. PRIORIDAD: ¿Existe logo_url (ImgBB)?


    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    # CORRECCIÓN 1: Usar corchetes y el nombre correcto de la clave
    c.drawString(margen_izq + 150, y_inicio - 25, datos['nombre_clinica'])

    # Datos Fiscales (Centro)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)

    # CORRECCIÓN 2: Concatenar usando f-strings y claves de diccionario
    direccion_1 = f"{datos['calle_y_numero']} {datos['colonia']}"
    c.drawString(margen_izq + 150, y_inicio - 40, direccion_1)

    c.setFont("Helvetica", 12)
    # CORRECCIÓN 3: Usar .get() para estado por si viene vacío
    direccion_2 = f"{datos['ciudad']} {datos.get('estado', '')}"
    c.drawString(margen_izq + 150, y_inicio - 55, direccion_2)

    c.setFont("Helvetica", 10)
    c.drawString(margen_izq + 150, y_inicio - 70, f"RFC: {datos['rfc']}")

    # ---------------------------------------------------------
    # 2. CAJA DE FOLIO Y FECHA (Derecha)
    # ---------------------------------------------------------
    x_folio = margen_izq + 410
    ancho_folio = 140

    c.setFillColor(color_fondo)
    c.roundRect(x_folio, y_inicio - 80, ancho_folio, 80, 5, fill=1, stroke=1)
    c.line(x_folio, y_inicio - 40, x_folio + ancho_folio, y_inicio - 40)

    # Sección FOLIO
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x_folio + (ancho_folio / 2), y_inicio - 15, "FOLIO")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_folio + 10, y_inicio - 32, "No.")
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(x_folio + ancho_folio - 15, y_inicio - 32, str(datos['folio']))

    # Sección FECHA
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x_folio + (ancho_folio / 2), y_inicio - 55, "FECHA")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x_folio + (ancho_folio / 2), y_inicio - 72, datos['fecha'])

    # ---------------------------------------------------------
    # 3. CUERPO DEL RECIBO (Datos)
    # ---------------------------------------------------------
    y_cuerpo = y_inicio - 90
    alto_cuerpo = 180

    c.setFillColor(color_fondo)
    c.roundRect(margen_izq, y_cuerpo - alto_cuerpo, ancho_util, alto_cuerpo, 5, fill=1, stroke=1)
    c.setFillColor(colors.black)

    # A. Recibimos de
    linea_1 = y_cuerpo - 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margen_izq + 10, linea_1, "Recibimos De(l) (la) Sr(a) :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen_izq + 160, linea_1, datos['recibido_de'])

    c.setStrokeColor(colors.gray)
    c.setLineWidth(0.5)
    c.line(margen_izq, linea_1 - 10, margen_izq + ancho_util, linea_1 - 10)

    # B. Nombre del interno
    linea_2 = linea_1 - 30
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(margen_izq + 10, linea_2, "Nombre del interno :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen_izq + 120, linea_2, datos['nombre_interno'])

    # C. Fechas (Del / Al)
    linea_3 = linea_2 - 25
    c.setFont("Helvetica", 10)
    c.drawString(margen_izq + 10, linea_3, "Del :")
    c.setFont("Helvetica", 10)
    # Usamos .get() por seguridad
    c.drawString(margen_izq + 40, linea_3, datos.get('periodo_inicio', ''))

    c.drawString(margen_izq + 200, linea_3, "Al :")
    c.drawString(margen_izq + 230, linea_3, datos.get('periodo_fin', ''))

    # D. Caja de Aportación
    linea_4 = linea_3 - 15
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(margen_izq, linea_4, margen_izq + ancho_util, linea_4)

    linea_dinero = linea_4 - 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margen_izq + 10, linea_dinero, "Aportacion voluntaria (no reembosable) :")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margen_izq + 250, linea_dinero, f"${datos['importe']:,.2f}")

    # Cantidad con letra
    linea_letra = linea_dinero - 20
    c.setFont("Helvetica", 9)
    c.drawString(margen_izq + 10, linea_letra, "Cantidad con letra :")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margen_izq + 10, linea_letra - 12, datos['importe_letra'])

    c.line(margen_izq, linea_letra - 20, margen_izq + ancho_util, linea_letra - 20)

    # E. Observaciones
    linea_obs = linea_letra - 40
    c.setFont("Helvetica", 10)
    c.drawString(margen_izq + 10, linea_obs, "Observaciones :")
    c.setFont("Helvetica", 10)
    c.drawString(margen_izq + 95, linea_obs, datos['observaciones'])

    if datos.get('cancelado'):
          c.saveState()
          c.translate(300, y_inicio - 100) # Mover al centro del recibo
          c.rotate(45) # Rotar 45 grados
          c.setFillColorRGB(0.8, 0, 0, 0.3) # Rojo transparente (Alpha 0.3)
          c.setFont("Helvetica-Bold", 60)
          c.drawCentredString(0, 0, "CANCELADO")
          c.restoreState()

def imprimir_recibo_pdf(request, id_recibo):
    # 1. Obtener datos de la BD
    recibo = get_object_or_404(Recibos, pk=id_recibo)

    try:
        clinica_actual = get_clinica_actual(request)
        # Obtenemos los datos generales de la clínica para el encabezado
        datosgrales = DatosGrales.objects.get(clinica=clinica_actual)

        interno = get_object_or_404(Internos, numeroexpediente=recibo.expediente, clinica=clinica_actual)

        nombre_interno = interno.nombrecompleto if interno else "NO ENCONTRADO"
        recibido_de = f"{interno.responsable}" if interno else "PARTICULAR"

        # Manejo seguro de fechas
        p_ini_txt = recibo.periodo_inicio.strftime("%d/%m/%Y") if recibo.periodo_inicio else ""
        p_fin_txt = recibo.periodo_fin.strftime("%d/%m/%Y") if recibo.periodo_fin else ""

        objeto_imagen_logo=None

        if datosgrales.logo_url:
            try:
                # Descargamos
                response = requests.get(datosgrales.logo_url, timeout=5)
                if response.status_code == 200:
                    # Convertimos a objeto ImageReader en memoria
                    img_bytes = io.BytesIO(response.content)
                    objeto_imagen_logo = ImageReader(img_bytes)
            except Exception as e:
                print(f"Error descargando logo: {e}")

            # B) Si no hay URL, intentamos local (logo_clinica)
        elif datosgrales.logo_clinica:
            try:
                objeto_imagen_logo = ImageReader(datosgrales.logo_clinica)
            except:
                pass


    except Exception as e:
        # Valores por defecto en caso de error (ej: no existen DatosGrales)
        nombre_interno = "DESCONOCIDO"
        recibido_de = "PARTICULAR"
        p_ini_txt = ""
        p_fin_txt = ""

        # Objeto dummy para que no falle el diccionario abajo
        class DummyGrales:
            nombre = "CLINICA"
            calleynumero = ""
            colonia = ""
            ciudad = ""
            estado = ""  # Agregado
            rfc = ""
            telefono = ""
            logo_url = ""
            cp=""

        datosgrales = DummyGrales()

    # Preparar diccionario de datos
    datos_recibo = {
        'folio': str(recibo.recibo).zfill(4),
        'expediente': interno.numeroexpediente,
        'fecha': recibo.fecha.strftime("%d/%m/%Y"),
        'recibido_de': recibido_de.upper(),
        'nombre_interno': nombre_interno.upper(),
        'importe': float(recibo.importe),
        'importe_letra': cantidad_con_letra(float(recibo.importe)),
        'observaciones': recibo.referencia or '',
        'periodo_inicio': p_ini_txt,
        'periodo_fin': p_fin_txt,

        # --- AQUÍ DEFINIMOS LAS CLAVES QUE USAMOS ARRIBA ---
        'nombre_clinica': datosgrales.nombre.upper(),
        'calle_y_numero': datosgrales.calleynumero.title(),
        'colonia': datosgrales.colonia.title(),
        'ciudad': datosgrales.ciudad.title(),
        'estado': getattr(datosgrales, 'estado', '').title(),  # AGREGADO: Asegúrate que tu modelo lo tenga
        'rfc': datosgrales.rfc,
        'telefono': datosgrales.telefono,
        'url_logo': datosgrales.logo_url,
        'codigo_postal':datosgrales.cp,
        'logo_objeto': objeto_imagen_logo,
        'cancelado': recibo.cancelado,

    }

    # 2. Configurar el PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle(f"Recibo_{recibo.recibo}")

    width, height = letter

    # 3. DIBUJAR LOS DOS RECIBOS
    # Primer Recibo
    y_arriba = height - 50
    dibujar_recibo(c, y_arriba, datos_recibo)

    # Línea de corte
    y_corte = height / 2
    c.setStrokeColor(colors.gray)
    c.setLineWidth(1)
    c.setDash(4, 4)
    c.line(20, y_corte, width - 20, y_corte)
    c.setDash()

    c.setFont("ZapfDingbats", 14)
    c.drawCentredString(width / 2, y_corte - 5, chr(34))

    # Segundo Recibo
    y_abajo = y_corte - 40
    dibujar_recibo(c, y_abajo, datos_recibo)

    # 4. Finalizar
    c.showPage()
    c.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def lista_recibos(request):
    clinica_actual = get_clinica_actual(request)
    mem_user_permisos = request.session.get('usuario_permisos')

    if 'OFICINA' not in mem_user_permisos and 'ADMIN' not in mem_user_permisos:
        messages.error(request, f"⛔ No tienes permisos para entrar aquí.")
        return redirect('Menu principal')

    # 1. QuerySet Base (Solo recibos de esta clínica)
    recibos = Recibos.objects.filter(clinica=clinica_actual).order_by('-recibo')  # Del más nuevo al viejo

    # 2. Filtros de Búsqueda
    busqueda = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha1')
    fecha_fin = request.GET.get('fecha2')

    if busqueda:
        # Busca por Folio, Expediente O Nombre del Operador
        recibos = recibos.filter(
            Q(recibo__icontains=busqueda) |
            Q(expediente__icontains=busqueda) |
            Q(nombreoperador__icontains=busqueda)
        )

    if fecha_inicio and fecha_fin:
        recibos = recibos.filter(fecha__range=[fecha_inicio, fecha_fin])

    # 3. Paginación (Mostrar 20 por página)
    paginator = Paginator(recibos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'busqueda': busqueda,
        'fecha1': fecha_inicio,
        'fecha2': fecha_fin
    }
    return render(request, 'lista_recibos.html', context)


from django.utils import timezone


def cancelar_recibo(request, id_recibo):
    if request.method != 'POST':
        return redirect('lista_recibos')  # Seguridad
    print(f"--- INTENTANDO CANCELAR RECIBO ID: {id_recibo} ---")  # DEBUG
    recibo = get_object_or_404(Recibos, pk=id_recibo)
    clinica_actual = get_clinica_actual(request)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    # Validaciones
    if recibo.cancelado:
        messages.warning(request, f"El recibo #{recibo.recibo} ya estaba cancelado.")
        return redirect('lista_recibos')

    try:
        with transaction.atomic():
            # 1. Obtener datos clave
            interno = Internos.objects.filter(numeroexpediente=recibo.expediente, clinica=clinica_actual).first()
            motivo = request.POST.get('motivo_cancelacion', 'Cancelación administrativa')

            # 2. Marcar Recibo como Cancelado
            recibo.cancelado = True
            recibo.fecha_cancelacion = timezone.now()
            recibo.usuario_cancela = mem_user_no
            recibo.usuario_cancela_nombre=mem_user_nombre
            recibo.motivo_cancelacion = motivo
            recibo.save()
            print("1. Recibo marcado como cancelado OK")  # DEBUG
            # 3. GENERAR CONTRA-MOVIMIENTO EN ESTADO DE CUENTA
            # Creamos un CARGO por el mismo monto para anular el abono original
            Edocuenta.objects.create(
                expediente=recibo.expediente,
                fecha=timezone.now().date(),
                concepto=4,
                referencia=f"CANCELACION RECIBO #{recibo.recibo}",
                importe=recibo.importe,  # <--- AQUÍ ESTÁ EL TRUCO: ES UN CARGO
                tipo='C'  # Tipo Cancelación o Cargo

            )
            print("2. Contra-movimiento creado OK")  # DEBUG
            # 4. ACTUALIZAR SALDO DEL PACIENTE
            # Si cancelamos un pago, la deuda vuelve a subir
            if interno:
                print(f"3. Interno encontrado: {interno.nombre}. Saldo actual: {interno.saldo}")  # DEBUG
                interno.saldo = float(interno.saldo) + float(recibo.importe)
                interno.save()
                print(f"4. Nuevo saldo guardado: {interno.saldo}")  # DEBUG

            messages.success(request, f"Recibo #{recibo.recibo} cancelado correctamente. Saldo actualizado.")

    except Exception as e:
        messages.error(request, f"Error al cancelar: {str(e)}")

    return redirect('lista_recibos')





# --- VISTA DEL MENÚ ---
def menu_reportes(request):
    return render(request, 'menu_reportes.html')


# --- FUNCIÓN AUXILIAR PARA DIBUJAR ENCABEZADOS Y PIE ---
def dibujar_encabezado(c, titulo, f1, f2, page_num):
    width, height = letter

    # Fondo Título
    c.setFillColor(colors.HexColor("#0d6efd"))  # Azul Bootstrap
    c.rect(0, height - 60, width, 60, fill=1, stroke=0)

    # Texto Título
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 40, titulo.upper())

    # Subtítulo Fechas
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 80, f"Del {f1} al {f2}")

    # Pie de página
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(30, 30, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.drawRightString(width - 30, 30, f"Página {page_num}")


# =========================================================
# REPORTE 1: CUOTAS RECIBIDAS (Basado en Recibos)
# =========================================================
def reporte_cuotas_recibidas(request):
    # 1. Obtener filtros
    f1 = request.GET.get('f1')
    f2 = request.GET.get('f2')
    clinica_actual = get_clinica_actual(request)

    # 2. Consultar Datos (Recibos NO cancelados)
    recibos = Recibos.objects.filter(
        clinica=clinica_actual,
        cancelado=False,
        fecha__range=[f1, f2]
    ).order_by('fecha', 'recibo')

    # Optimización: Obtener nombres de pacientes en un diccionario
    # { 'EXP001': 'JUAN PEREZ', ... }
    exps = recibos.values_list('expediente', flat=True)
    mapa_nombres = {
        i.numeroexpediente: i.nombrecompleto
        for i in Internos.objects.filter(numeroexpediente__in=exps, clinica=clinica_actual)
    }

    # 3. Configurar PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 120  # Posición inicial Y
    page_num = 1
    total_gral = 0

    dibujar_encabezado(c, "REPORTE DE CUOTAS RECIBIDAS", f1, f2, page_num)

    # Encabezados de Tabla
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, "FECHA")
    c.drawString(100, y, "FOLIO")
    c.drawString(160, y, "PACIENTE / EXPEDIENTE")
    c.drawString(400, y, "REFERENCIA")
    c.drawRightString(580, y, "IMPORTE")
    c.line(30, y - 5, 580, y - 5)
    y -= 20

    # 4. Imprimir Filas
    c.setFont("Helvetica", 9)

    for r in recibos:
        # Verificar salto de página
        if y < 50:
            c.showPage()
            page_num += 1
            y = height - 120
            dibujar_encabezado(c, "REPORTE DE CUOTAS RECIBIDAS", f1, f2, page_num)
            # Re-imprimir encabezados tabla
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y, "FECHA")
            c.drawString(100, y, "FOLIO")
            c.drawRightString(580, y, "IMPORTE")
            c.line(30, y - 5, 580, y - 5)
            y -= 20
            c.setFont("Helvetica", 9)

        # Datos
        nombre = mapa_nombres.get(r.expediente, "DESCONOCIDO")

        c.drawString(30, y, r.fecha.strftime("%d/%m/%Y"))
        c.drawString(100, y, str(r.recibo))
        c.drawString(160, y, f"{nombre[:30]} ({r.expediente})")  # Recorta nombre largo
        c.drawString(400, y, r.referencia[:25] if r.referencia else "")
        c.drawRightString(580, y, f"${r.importe:,.2f}")

        total_gral += r.importe
        y -= 15

    # 5. Total Final
    c.line(30, y + 5, 580, y + 5)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y - 15, "TOTAL RECIBIDO:")
    c.drawRightString(580, y - 15, f"${total_gral:,.2f}")

    c.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


# =========================================================
# REPORTE 2: CUOTAS POR RECIBIR (Basado en Edocuenta Cargo)
# =========================================================
def reporte_cuotas_por_recibir(request):
    f1 = request.GET.get('f1')
    f2 = request.GET.get('f2')
    clinica_actual = get_clinica_actual(request)

    # Buscamos en Edocuenta donde haya CARGO > 0 (Es deuda programada)
    # Excluimos Cancelaciones si tu sistema usa 'C' para cancelar y cargo para deuda
    # Ajusta el filtro según tu lógica: cargo > 0 suele ser suficiente para "Deuda"
    cuotas = Edocuenta.objects.filter(
        # clinica=clinica_actual, # Descomenta si Edocuenta tiene campo clinica
        referencia__startswith='Cuota #',
        fecha__range=[f1, f2]
    ).exclude(concepto__icontains="CANCELACION").order_by('fecha')

    # Mapa de nombres
    exps = cuotas.values_list('expediente', flat=True)
    mapa_nombres = {
        i.numeroexpediente: i.nombrecompleto
        for i in Internos.objects.filter(numeroexpediente__in=exps, clinica=clinica_actual)
    }

    # Configurar PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 120
    page_num = 1
    total_gral = 0

    dibujar_encabezado(c, "CUOTAS POR RECIBIR (PROGRAMADAS)", f1, f2, page_num)

    # Encabezados
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, "FECHA PROG.")
    c.drawString(120, y, "EXPEDIENTE / PACIENTE")
    c.drawString(400, y, "CONCEPTO")
    c.drawRightString(580, y, "MONTO ESPERADO")
    c.line(30, y - 5, 580, y - 5)
    y -= 20

    c.setFont("Helvetica", 9)

    for row in cuotas:
        if y < 50:
            c.showPage()
            page_num += 1
            y = height - 120
            dibujar_encabezado(c, "CUOTAS POR RECIBIR", f1, f2, page_num)
            c.setFont("Helvetica-Bold", 10)
            c.drawRightString(580, y, "MONTO")
            y -= 20
            c.setFont("Helvetica", 9)

        nombre = mapa_nombres.get(row.expediente, "DESCONOCIDO")

        c.drawString(30, y, row.fecha.strftime("%d/%m/%Y"))
        c.drawString(120, y, f"{row.expediente} - {nombre[:35]}")
        c.drawString(400, y, row.referencia)
        c.drawRightString(580, y, f"${row.importe:,.2f}")

        total_gral += row.importe
        y -= 15

    c.line(30, y + 5, 580, y + 5)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y - 15, "TOTAL POR RECIBIR:")
    c.drawRightString(580, y - 15, f"${total_gral:,.2f}")

    c.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')