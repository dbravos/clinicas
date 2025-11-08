from django.db.models import Q
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import request, Http404, HttpResponse
from django.contrib import messages
from datetime import datetime,date
from django.core.exceptions import ValidationError
from django.db import transaction,DatabaseError
import logging
import json
import os
import requests
from reportlab.pdfgen import canvas  # ✅ AGREGAR ESTA IMPORTACIÓN
from reportlab.lib.pagesizes import letter  # ✅ Y ESTA TAMBIÉN
from django.http import HttpResponse
from django.conf import settings
from datetime import date, timedelta

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
                        NotasEvolucionPS,Medico,Recetas,HistoriaClinica,Clinicas

from .formas import DatosGralesf,Usuariosf,Internosf,IntResponsablef,IntDependientesf,IntProvienef,Einicialf,\
                    Assistf,SituacionFamiliarf,Cfisicasf,Cmentalesf,Crelacionesf,Tratamientosf,Psicosisf,Sdevidaf,\
                    Usodrogasf,Ansiedadf,Depresionf,Marcadoresf,Riesgosf,Razonesf,Valorizacionf,\
                    CIndividualf,CFamiliarf,CGrupalf,PConsejeriaf,TareaConsejeriaf,HojaAtencionPsf,NotasEvolucionPSf,\
                    Medicof,Recetasf,HistoriaClinicaf,ClinicaLoginForm




logger = logging.getLogger(__name__)

# Create your views here.

def home_temp(request):
    return HttpResponse("¡Mi Django funciona en Railway! 🚀")

def get_clinica_actual(request):
    return request.session.get('clinica_actual', 'Demostracion')

def primermenu(request):

    interno = Internos.objects.first()
    return render(request,'MenuPrincipal.html', {'interno': interno})

def imprime_contrato(request,id):
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.first()

    return render(request,'imprime_contrato.html', {'interno': interno,'datosgrales':datosgrales})

def imprime_solicitud(request,id):
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.first()

    return render(request,'solicitud_internacion.html', {'interno': interno,'datosgrales':datosgrales})

def imprime_aviso(request,id):
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.first()
    # En tu vista


    if interno.fechaingreso:
        # Formatear la fecha como "17 de FEBRERO del 2024"
       meses = {
        1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
        5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
        9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
    }
       fecha_formateada = f"{interno.fechaingreso.day} de {meses[interno.fechaingreso.month]} del {interno.fechaingreso.year}"

       return render(request, 'aviso_internacion.html', {
               'interno': interno,
               'datosgrales': datosgrales,
               'fecha_formateada': fecha_formateada  # ¡Aquí la agregas!
                })
    else:
        return render(request, 'aviso_internacion.html', {
               'interno': interno,
               'datosgrales': datosgrales,
               'fecha_formateada': "FECHA NO DISPONIBLE"
           })


# En tu vista de consentimiento
def consentimiento(request, id):
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.first()  # O como obtengas estos datos

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

def grabainterno(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id, clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    intresponsablef=IntResponsablef(request.POST,instance=interno)
    intdependientesf = IntDependientesf(request.POST, instance=interno)
    intprovienef =IntProvienef(request.POST,instance=interno)
    interno.nombrecompleto=f"{interno.nombre} {interno.apaterno} {interno.amaterno}"
    interno.comentarios = request.POST.get('comentarios', '')
    if all([internof.is_valid(),intresponsablef.is_valid(),intdependientesf.is_valid(),intprovienef.is_valid()]) :
       internof.save()
       intresponsablef.save()
       intdependientesf.save()
       intprovienef.save()

       messages.success(request,'Actualizacion existosa '+str(interno.numeroexpediente))
    else:
       messages.error(request,'No se Actualizo ' + str(id))
    try:
        with transaction.atomic():
            interno.save()
    except Exception as e:
        messages.error(request, f'Error durante la actualización: {str(e)}')

    internos = Internos.objects.filter(clinica=clinica_actual).order_by('numeroexpediente')

    return render(request, 'listar.html', {'internos': internos})

def registro(request):
    return render(request,'registro.html')


def datosgrales(request):
    clinica_actual = get_clinica_actual(request)

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


    datosgralesf = DatosGralesf(instance=datosgrales)
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

    if request.method == 'POST':
        # DEBUG: Ver qué llega en el request
        print(f"📨 POST keys: {list(request.POST.keys())}")
        print(f"📁 FILES keys: {list(request.FILES.keys())}")

        datosgralesf = DatosGralesf(request.POST, request.FILES, instance=datosgrales)

        if datosgralesf.is_valid():
            instance = datosgralesf.save(commit=False)

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
    mem_user_permisos = request.session.get('usuario_permisos')


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

def grabadatosusuario(request,id):

    clinica_actual=get_clinica_actual(request)
    usuario = Usuarios.objects.get(usuario=id,clinica=clinica_actual)
    usuariof= Usuariosf(request.POST,instance=usuario)
    if usuariof.is_valid():
        usuariof.save()
        messages.success(request,'Actualizacion existosa '+str(usuario.usuario))
    else:
        messages.error(request,'No se Actualizo ' + str(id))

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

def consentimientoold(request,id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="consentimiento.pdf"'
    interno = get_object_or_404(Internos, pk=id)
    datosgrales = DatosGrales.objects.first()
    archivo_pdf="consentimiento.pdf"
    # Crear un canvas de ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica", 10)

    mSuperior=760
    mizquierdo =50
    avance=15
    # Agregar un título al reporte



    logo_path = os.path.join(settings.BASE_DIR, 'mapp','static', 'images', 'logo.jpg')

    p.drawImage(logo_path,10,680,width=120,height=100)
    p.drawString(140,mSuperior,datosgrales.nombre)
    p.drawString(140,mSuperior-avance,'RFC : '+datosgrales.rfc)
    p.drawString(140,mSuperior-2*avance,datosgrales.calleynumero+','+datosgrales.colonia)
    p.drawString(140,mSuperior-3*avance,datosgrales.ciudad+' '+datosgrales.estado+','+datosgrales.cp)
    p.drawString(140,mSuperior-4*avance,'WEB: '+datosgrales.sitioweb+'   Email :'+datosgrales.correoelectronico)
    p.drawString(140,mSuperior-5*avance,'Telefono: '+datosgrales.telefono)
    p.drawString(420,mSuperior-6*avance,'Expediente : '+interno.numeroexpediente)
    fecha_y_hora=datetime.now()
    p.drawString(420,mSuperior-7*avance,'Fecha y Hora :'+fecha_y_hora.strftime("%d/%m/%Y  %I:%M %p"))

    p.setFont("Helvetica", 14)
    p.drawString(220,mSuperior-10*avance, "Consentimiento Informado")
    p.setFont("Helvetica", 8)
    p.drawString(10, mSuperior - 12 * avance, 'C. DIRECTOR O RESPONSABLE DEL ESTABLECIMIENTO')
    p.drawString(10, mSuperior - 13 * avance, 'PRESENTE')
    p.drawString(10, mSuperior - 15 * avance, 'EL(LA) QUE SUSCRIBE C. '+interno.nombrecompleto)
    p.drawString(10, mSuperior - 16 * avance, 'OTORGADO MI CONSENTIMIENTO PARA RECIBIR EL TRATAMIENTO EL CUAL CONSISTE EN: REUNIONES Y SESIONES DE LOS 12 PASOS DE')
    p.drawString(10, mSuperior - 17 * avance, 'N.A. TERAPIA OCUPACIONAL,TRATAMIENTO PSICOLOGICO Y DIVERSAS ACTIVIDADES')
    p.drawString(10, mSuperior - 18 * avance, 'CON  UNA DURACION DE '+ str(interno.duracion))
    p.drawString(10, mSuperior - 19 * avance, 'HACIENDO CONSTAR QUE FUI INFORMADO DE TO0OS Y CADA UNO DE LOS PROCEDIMIENTOS, IMPLICACIONES Y RIESGOS QUE ESTE')
    p.drawString(10, mSuperior - 20 * avance, 'IMPLICA, ASI COMO LOS ESTATUTOS, REGLAMENTO INTERNO Y DE LAS CONDICIONES DE INGRESO, ESTANCIA Y EGRESO DEL')
    p.drawString(10, mSuperior - 21 * avance, 'ESTABLECIMIENTO, INFORMACION QUE ME FUE PROPORCIONADA DETALLADAMENTE POR EL O LA C. RESPONSABLE DEL CENTRO')
    p.drawString(10, mSuperior - 22 * avance, 'DE TRATAMIENTO '+datosgrales.nombre)
    p.drawString(30, mSuperior - 24 * avance, 'LO ANTERIOR APEGADO A LO DISPUESTO EN EL APARTADO 10.3.1 DE LA NORMA OFICIAL MEXICANA NOM-028-2009, PARA LA ')
    p.drawString(10, mSuperior - 25 * avance, 'PREVENCION , TRATAMIENTO Y CONTROL DE ADICCIONES')
    p.drawString(85, mSuperior - 28 * avance, 'USUARIO(A)')
    p.drawString(305, mSuperior - 28 * avance, 'FAMILIAR O RESPONSABLE')
    p.drawString(60, mSuperior - 31 * avance, '________________  _____________')
    p.drawString(300, mSuperior - 31 * avance, '_______________  _____________')
    p.drawString(60, mSuperior - 32 * avance, '       Nombre                    Firma')
    p.drawString(300, mSuperior - 32 * avance, '      Nombre                    Firma')
    p.drawString(300, mSuperior - 33 * avance, 'Parentesco o Relacion :___________')
    p.drawString(220, mSuperior - 36 * avance, 'ENCARGADO DEL ESTABLECIMIENTO')
    p.drawString(220, (mSuperior-1) - (39 * avance), datosgrales.responsable)
    p.drawString(220, mSuperior - 39 * avance, '________________        __________________')
    p.drawString(220, mSuperior - 40 * avance, '     Nombre                               Firma')

    # Finalizar el PDF
    p.showPage()
    p.save()

    try:
        impresora_default = win32print.GetDefaultPrinter()
        win32api.ShellExecute(0, "print", archivo_pdf, None, ".", 0)
    except Exception as e:
        print(f"Error al imprimir: {e}")

    #os.remove(archivo_pdf)

    return response


def einicial(request, id):
    clinica_actual=get_clinica_actual(request)
    # Obtener el interno
    interno = get_object_or_404(Internos, pk=id, clinica=clinica_actual)


    # Obtener o crear registros
    try:
        einicial = get_object_or_404(Einicial, expediente=interno.numeroexpediente,clinica=clinica_actual)
    except Http404:
        # Crear registros si no existen
        einicial = Einicial.objects.create(expediente=interno.numeroexpediente,clinica=clinica_actual)
    try:
        situacionfamiliar = get_object_or_404(SituacionFamiliar, expediente=interno.numeroexpediente,clinica=clinica_actual)
    except Http404:
        situacionfamiliar = SituacionFamiliar.objects.create(expediente=interno.numeroexpediente,clinica=clinica_actual)
    try:
        cfisicas = get_object_or_404(Cfisicas, expediente=interno.numeroexpediente,clinica=clinica_actual)
    except Http404:
        cfisicas = Cfisicas.objects.create(expediente=interno.numeroexpediente,clinica=clinica_actual)
    try:
        cmentales = get_object_or_404(Cmentales, expediente=interno.numeroexpediente,clinica=clinica_actual)
    except Http404:
        cmentales = Cmentales.objects.create(expediente=interno.numeroexpediente,clinica=clinica_actual)
    try:
        crelaciones = get_object_or_404(Crelaciones, expediente=interno.numeroexpediente,clinica=clinica_actual)
    except Http404:
        crelaciones = Crelaciones.objects.create(expediente=interno.numeroexpediente,clinica=clinica_actual)
    try:
        tratamientos = get_object_or_404(Tratamientos, expediente=interno.numeroexpediente,clinica=clinica_actual)
    except Http404:
        tratamientos = Tratamientos.objects.create(expediente=interno.numeroexpediente,clinica=clinica_actual)
    try:
        valorizacion = get_object_or_404(Valorizacion, expediente=interno.numeroexpediente,clinica=clinica_actual)
    except Http404:
        valorizacion = Valorizacion.objects.create(expediente=interno.numeroexpediente,clinica=clinica_actual)

    # Manejo de POST
    if request.method == "POST":
        einicialf = Einicialf(request.POST, instance=einicial)
        situacionfamiliarf = SituacionFamiliarf(request.POST, instance=situacionfamiliar)
        cfisicasf = Cfisicasf(request.POST, instance=cfisicas)
        cmentalesf = Cmentalesf(request.POST, instance=cmentales)
        crelacionesf = Crelacionesf(request.POST, instance=crelaciones)
        tratamientosf = Tratamientosf(request.POST, instance=tratamientos)
        valorizacionf = Valorizacionf(request.POST, instance=valorizacion)

        if all(form.is_valid() for form in
               [einicialf, situacionfamiliarf, cfisicasf, cmentalesf, crelacionesf, tratamientosf, valorizacionf]):
            with transaction.atomic():
                einicialf.save()
                situacionfamiliarf.save()
                cfisicasf.save()
                cmentalesf.save()
                crelacionesf.save()
                tratamientosf.save()
                valorizacionf.save()

            messages.success(request, 'Datos actualizados correctamente')
            return redirect('einicial', id=id,clinica=clinica_actual)  # Redirige a otra vista diferente
    else:
         # Manejo de GET (o POST con errores)
         einicialf = Einicialf(instance=einicial)
         situacionfamiliarf = SituacionFamiliarf(instance=situacionfamiliar)
         cfisicasf = Cfisicasf(instance=cfisicas)
         cmentalesf = Cmentalesf(instance=cmentales)
         crelacionesf = Crelacionesf(instance=crelaciones)
         tratamientosf = Tratamientosf(instance=tratamientos)
         valorizacionf = Valorizacionf(instance=valorizacion)

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
        'situaciones': situaciones
    }
    return render(request, 'einicialnw.html',context)

def grabaeinicial(request, id):

    clinica_actual=get_clinica_actual(request)

    try:
        interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)

        if not interno.numeroexpediente:
            messages.error(request, "El interno no tiene número de expediente asignado")
            return redirect('selecciona')

        modelos = {
            'einicial': Einicial,
            'situacionfamiliar': SituacionFamiliar,
            'cfisicas': Cfisicas,
            'cmentales': Cmentales,
            'crelaciones': Crelaciones,
            'tratamientos': Tratamientos,

        }
        mem_user_no = request.session.get('usuario_no')
        mem_user_nombre = request.session.get('usuario_nombre')
        mem_user_permisos = request.session.get('usuario_permisos')

        with transaction.atomic():
            instancias = {}
            for nombre_modelo, modelo in modelos.items():
                try:
                    instancia, created = modelo.objects.get_or_create(
                        expediente=interno.numeroexpediente,
                        clinica=clinica_actual,
                        defaults={'expediente': interno.numeroexpediente, 'consejero':mem_user_no,}
                    )
                    if created:
                        instancia.full_clean()
                        instancia.save()
                    instancias[nombre_modelo] = instancia
                except Exception as e:
                    logger.error(f"Error creando {nombre_modelo}: {str(e)}")
                    raise

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
                            instance = form.save(commit=False)  # ← Objeto en memoria
                            form.instance.expediente=interno.numeroexpediente
                            form.instance.clinica=clinica_actual
                            form.save()
                    messages.success(request, 'Datos guardados correctamente')
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
            **forms,
            **instancias

        }
        return render(request, 'einicialnw.html', context)

    except DatabaseError as e:
        messages.error(request, "Error de base de datos. Contacte al administrador.")
        logger.error(f"DatabaseError: {str(e)}")
        return redirect('einicial', id=id)
    except ValidationError as e:
        messages.error(request, f"Error de validación: {str(e)}")
        logger.error(f"ValidationError: {e.message_dict}")
        return redirect('einicial', id=id)
    except Exception as e:
         error_details = {
              'exception_type': type(e).__name__,
              'error_message': str(e),
              'form_errors': {name: form.errors.as_json() for name, form in forms.items() if hasattr(form, 'errors')},
              'post_data': request.POST.dict()
               }
         logger.exception(f"ERROR DETALLADO: {json.dumps(error_details, indent=2)}")
         messages.error(request, f"Error crítico en el formulario. Ver logs para detalles.")
         return redirect('einicial', id=id)


def assist(request,id):

    clinica_actual=get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

    try:
        assist = Assist.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        assistf = Assistf(instance=assist)

    except Assist.DoesNotExist:
        assist = Assist(expediente=interno.numeroexpediente)
        assist.consejero = mem_user_no
        assist.clinica = clinica_actual
        assist.save()
        assistf = Assistf(instance=assist)
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        valorizacionf = Valorizacionf(instance=valorizacion)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion(expediente=interno.numeroexpediente)
        valorizacion.clinica=clinica_actual
        valorizacion.save()
        valorizacionf = Valorizacionf(instance=valorizacion)

    return render(request, 'assist.html', {'assist': assist, 'assistf':assistf,'interno':interno,'valorizacion':valorizacion,'valorizacionf':valorizacionf} )

def grabalo(request, id):

    clinica_actual = get_clinica_actual(request)
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
                        defaults={'expediente': interno.numeroexpediente}
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

def psicosis(request,id):

    clinica_actual=get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    try:
        psicosis = Psicosis.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        psicosisf = Psicosisf(instance=psicosis)
    except Psicosis.DoesNotExist:
        psicosis = Psicosis(expediente=interno.numeroexpediente)
        psicosis.psconsejero = mem_user_no
        psicosis.clinica = clinica_actual
        psicosis.save()
        psicosisf = Psicosisf(instance=psicosis)
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        valorizacionf = Valorizacionf(instance=valorizacion)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion(expediente=interno.numeroexpediente)
        valorizacion.clinica=clinica_actual
        valorizacion.save()
        valorizacionf = Valorizacionf(instance=valorizacion)

    return render(request, 'psicosis.html', {'psicosis': psicosis, 'psicosisf':psicosisf,'interno':interno,'valorizacion':valorizacion,'valorizacionf':valorizacionf} )

def sdevida(request, id):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id, clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

    # Sdevida - obtener o crear
    try:
        sdevida = Sdevida.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Sdevida.DoesNotExist:
        sdevida = Sdevida.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            svconsejero=mem_user_no
        )
    sdevidaf = Sdevidaf(instance=sdevida)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

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

    # Usodrogas - obtener o crear
    try:
        usodrogas = Usodrogas.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Usodrogas.DoesNotExist:
        usodrogas = Usodrogas.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            udconsejero=mem_user_no
        )
    usodrogasf = Usodrogasf(instance=usodrogas)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

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

    # Ansiedad - obtener o crear
    try:
        ansiedad = Ansiedad.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Ansiedad.DoesNotExist:
        ansiedad = Ansiedad.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            anconsejero=mem_user_no
        )
    ansiedadf = Ansiedadf(instance=ansiedad)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

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

    # Depresion - obtener o crear
    try:
        depresion = Depresion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Depresion.DoesNotExist:
        depresion = Depresion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            depconsejero=mem_user_no
        )
    depresionf = Depresionf(instance=depresion)

    # Valorizacion - obtener o crear
    try:
        valorizacion = Valorizacion.objects.get(expediente=interno.numeroexpediente, clinica=clinica_actual)
    except Valorizacion.DoesNotExist:
        valorizacion = Valorizacion.objects.create(
            expediente=interno.numeroexpediente,
            clinica=clinica_actual,
            valorizacionconsejero=mem_user_no
        )
    valorizacionf = Valorizacionf(instance=valorizacion)

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

    try:
        marcadores = Marcadores.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        marcadoresf = Marcadoresf(instance=marcadores)
    except Marcadores.DoesNotExist:
        marcadores=Marcadores(expediente=interno.numeroexpediente)
        marcadores.marconsejero = mem_user_no
        marcadores.clinica = clinica_actual
        marcadores.save()
        marcadoresf=Marcadoresf(instance=marcadores)

    return render(request, 'marcadores.html', {'marcadores': marcadores, 'marcadoresf':marcadoresf,'interno':interno} )

def riesgos(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

    try:
        riesgos = Riesgos.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        riesgosf = Riesgosf(instance=riesgos)
    except Riesgos.DoesNotExist:
        riesgos=Riesgos(expediente=interno.numeroexpediente)
        riesgos.riesgoconsejero = mem_user_no
        riesgos.clinica = clinica_actual
        riesgos.save()
        riesgosf=Riesgosf(instance=riesgos)

    return render(request, 'riesgos.html', {'riesgos': riesgos, 'riesgosf':riesgosf,'interno':interno} )

def razones(request,id):

    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(pk=id,clinica=clinica_actual)
    internof= Internosf(request.POST,instance=interno)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

    try:
        razones = Razones.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        razonesf = Razonesf(instance=razones)
    except Razones.DoesNotExist:
        razones=Razones(expediente=interno.numeroexpediente)
        razones.razonesconsejero = mem_user_no
        razones.clinica = clinica_actual
        razones.save()
        razonesf=Razonesf(instance=razones)

    return render(request, 'razones.html', {'razones': razones, 'razonesf':razonesf,'interno':interno} )


def valorizacion(request,id):

    clinica_actual = get_clinica_actual(request)
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


def grabanew(request, id, modelos_config, forms_config, template_name, redirect_view, modelo_principal=Internos):
    clinica_actual = get_clinica_actual(request)
    principal = get_object_or_404(modelo_principal, pk=id, clinica=clinica_actual)
    forms = {}
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

    try:
        # 1. Obtener o crear instancias
        instancias = {}
        with transaction.atomic():
            for nombre_modelo, (modelo, principal_lookup, related_lookup) in modelos_config.items():
                lookup_value = getattr(principal, principal_lookup)
                lookup_kwargs = {related_lookup: lookup_value, 'clinica': clinica_actual}
                instancia, created = modelo.objects.get_or_create(
                    **lookup_kwargs,
                    defaults={**lookup_kwargs, 'consejero': mem_user_no}
                )
                instancias[nombre_modelo] = instancia

        # 2. Inicializar formularios
        for form_name, (form_class, related_name) in forms_config.items():
            instance = instancias.get(related_name)
            forms[form_name] = form_class(request.POST or None, instance=instance)

        # 3. Manejar POST
        if request.method == "POST":
            if all(form.is_valid() for form in forms.values()):
                try:
                    with transaction.atomic():
                        for form_name, form in forms.items():
                            if form.has_changed():
                                related_name = [rn for fn, (_, rn) in forms_config.items() if fn == form_name][0]
                                _, principal_lookup, related_lookup = modelos_config[related_name]

                                # Asignar valores antes de guardar
                                valor_principal = getattr(principal, principal_lookup)
                                setattr(form.instance, related_lookup, valor_principal)
                                setattr(form.instance, 'clinica', clinica_actual)
                                setattr(form.instance, 'consejero', mem_user_no)

                                form.save()
                                logger.info(f"Formulario '{form_name}' guardado")

                    messages.success(request, 'Datos guardados correctamente')
                    return redirect('seleccionainterno', id=id)  # ← REDIRIGE A UNA VISTA DIFERENTE

                except Exception as e:
                    messages.error(request, f"Error al guardar: {str(e)}")
                    logger.exception("Error al guardar formularios")
            else:
                messages.error(request, 'No se pudo guardar. Por favor, corrija los errores.')
                for form_name, form in forms.items():
                    if form.errors:
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, f"Error en {form_name} - {field}: {error}")

        # 4. Renderizar template (SIEMPRE)
        context = {
            'interno': principal,
            **forms,
            **instancias
        }
        return render(request, template_name, context)

    except Exception as e:
        logger.exception(f"ERROR en grabanew: {str(e)}")
        messages.error(request, "Error crítico en el formulario.")
        return redirect('seleccionainterno',id=id)  # ← REDIRIGE A UNA VISTA DIFERENTE


def assist_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'assist': (Assist, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'assistf': (Assistf, 'assist')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'assist.html',
        'graba-assist', # El nombre de la URL para la redirección
        Internos
    )
def psicosis_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'psicosis': (Psicosis, 'numeroexpediente', 'expediente'),

    }

    # Esta configuración no cambia
    forms_config = {
        'psicosisf': (Psicosisf, 'psicosis'),

    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'psicosis.html',
        'graba-psicosis', # El nombre de la URL para la redirección
        Internos,

    )
def sdevida_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'sdevida': (Sdevida, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'sdevidaf': (Sdevidaf, 'sdevida')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'satisfaccion.html',
        'graba-sdevida', # El nombre de la URL para la redirección
        Internos
    )

def usodrogas_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'usodrogas': (Usodrogas, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'usodrogasf': (Usodrogasf, 'usodrogas')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'usodrogas.html',
        'graba-usodrogas', # El nombre de la URL para la redirección
        Internos
    )
def ansiedad_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'ansiedad': (Ansiedad, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'ansiedadf': (Ansiedadf, 'ansiedad')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'ansiedad.html',
        'graba-ansiedad', # El nombre de la URL para la redirección
        Internos
    )
def depresion_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'depresion': (Depresion, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'depresionf': (Depresionf, 'depresion')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'depresion.html',
        'graba-depresion', # El nombre de la URL para la redirección
        Internos
    )

def marcadores_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'marcadores': (Marcadores, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'marcadoresf': (Marcadoresf, 'marcadores')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'marcadores.html',
        'graba-marcadores', # El nombre de la URL para la redirección
        Internos
    )
def riesgos_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'riesgos': (Riesgos, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'riesgosf': (Riesgosf, 'riesgos')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'riesgos.html',
        'graba-riesgos', # El nombre de la URL para la redirección
        Internos
    )


def razones_cfg(request, id):
    """
    Configuración para la vista de Assist.
    """
    # <-- CAMBIO: La tupla ahora tiene 3 elementos
    # (ModeloRelacionado, 'campo_en_Internos', 'campo_en_Assist')
    modelos_config = {
        'razones': (Razones, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'razonesf': (Razonesf, 'razones')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'razones.html',
        'graba-razones', # El nombre de la URL para la redirección
        Internos
    )
def valorizacion_cfg(request, id):

    modelos_config = {
        'valorizacion': (Valorizacion, 'numeroexpediente', 'expediente')
    }

    # Esta configuración no cambia
    forms_config = {
        'valorizacionf': (Valorizacionf, 'valorizacion')
    }

    return grabanew(
        request,
        id,
        modelos_config,
        forms_config,
        'dgenerales.html',
        'graba-valorizacion', # El nombre de la URL para la redirección
        Internos,
    )




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

    interno = Internos.objects.get(numeroexpediente=id, clinica=clinica_actual)
    mapping = MODEL_FORM_MAP.get(tipo_sesion)
    if not mapping:
        return render(request, 'error.html', {'message': 'Tipo de sesión no válido.'})

    modelo = mapping['model']
    verbose_name = mapping['verbose_name']
    form_class = mapping['form_class']

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
        'interno':interno,
    }
    return render(request, 'lista_sesiones.html', context)


from datetime import date


def capturaSesion(request, tipo_sesion, accion, id=None, no_sesion=None):
    clinica_actual = get_clinica_actual(request)
    interno = Internos.objects.get(numeroexpediente=id, clinica=clinica_actual)

    print(f'sesion={tipo_sesion}, id_interno_pk={id}, numero_expediente={interno.numeroexpediente}, accion={accion}, no_sesion={no_sesion}')

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
       print(f"🔍 DEBUG CRÍTICO:")
       print(f"   interno.numeroexpediente: '{interno.numeroexpediente}'")
       print(f"   clinica_actual: '{clinica_actual}'")
       print(f"   Tipo de expediente: {type(interno.numeroexpediente)}")
       print(f"   Tipo de clinica: {type(clinica_actual)}")

            # Verificar con valores directos
       existe_con_valores_directos = modelo.objects.filter(
             expediente='000002',
                sesion=1,
                clinica=clinica_actual
            ).exists()
       print(f"   ¿Existe con valores directos?: {existe_con_valores_directos}")

       # Verificar solo por expediente
       existe_solo_expediente = modelo.objects.filter(expediente='000002', sesion=1).exists()
       print(f"   ¿Existe solo por expediente?: {existe_solo_expediente}")




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

            # 🔥 GUARDAR PARA AMBOS CASOS (agregar Y editar)
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
        instancia_sesion = None

    if request.method == 'POST':
        form = form_class(request.POST, instance=instancia_sesion)
        if form.is_valid():
            sesion_guardar = form.save(commit=False)
            sesion_guardar.expediente = interno.numeroexpediente
            sesion_guardar.psicologo = mem_user_no
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






def listaSesionesGrupales(request,id=None):
    """
    Vista para listar todas las sesiones grupales
    """
    clinica_actual = get_clinica_actual(request)
    sesiones_grupales = CGrupal.objects.filter(clinica=clinica_actual).order_by('-fecha', '-sesion')

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



def planConsejeria(request, id):
    """
    Obtiene el interno por ID y luego busca/crea su consejería
    """
    # 1. Obtener el interno
    clinica_actual = get_clinica_actual(request)
    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')

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
        print("=== DEBUG: POST recibido ===")
        print(f"=== DEBUG: Datos POST: {request.POST} ===")  # Ver qué datos llegan

        # Crear el formulario con los datos del POST y la instancia existente
        hatencionpsf = HojaAtencionPsf(request.POST, instance=hatencionps)

        print(f"Formulario válido: {hatencionpsf.is_valid()}")

        if hatencionpsf.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = hatencionpsf.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente
            saved_instance.clinica=clinica_actual# Asegurar el expediente
            saved_instance.psicologo=mem_user_no # Asegurar el expediente
            saved_instance.save()

            print(f"=== DEBUG: Guardado exitoso - ID: {saved_instance.id} ===")
            print(f"=== DEBUG: Expediente guardado: {saved_instance.expediente} ===")
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
    interno = get_object_or_404(Internos, pk=id,clinica=clinica_actual)
    mem_user_no = request.session.get('usuario_no')
    mem_user_nombre = request.session.get('usuario_nombre')
    # 2. Buscar consejería existente o crear una nueva
    try:
        # Primero intentar obtener una existente
        medicoinicial = Medico.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False
        print(f"=== DEBUG: Plan existente encontrado - ID: {medicoinicial.id} ===")
        print(f"=== DEBUG: con expediente : {medicoinicial.expediente} ===")

    except Medico.DoesNotExist:
        # Si no existe, crear una nueva
        medicoinicial = Medico(expediente=interno.numeroexpediente)
        medicoinicial.medico = mem_user_no
        medicoinicial.clinica = clinica_actual

        medicoinicial.save()
        creado = True
        print(f"=== DEBUG: Nuevo plan creado - ID: {medicoinicial.id} ===")
        print(f"=== DEBUG: con expediente : {medicoinicial.expediente} ===")
    except Medico.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        medicoinicial = Medico.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).latest('id')
        creado = False
        print(f"=== DEBUG: Múltiples planes, tomando el más reciente - ID: {medicoinicial.id} ===")

    if request.method == 'POST':
        print("=== DEBUG: POST recibido ===")
        print(f"=== DEBUG: Datos POST: {request.POST} ===")  # Ver qué datos llegan

        # Crear el formulario con los datos del POST y la instancia existente
        medicof = Medicof(request.POST, instance=medicoinicial)

        print(f"Formulario válido: {medicof.is_valid()}")

        if medicof.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = medicof.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente  # Asegurar el expediente
            saved_instance.clinica = clinica_actual  # Asegurar el expediente
            saved_instance.medico = mem_user_no  # Asegurar el expediente

            saved_instance.save()

            print(f"=== DEBUG: Guardado exitoso - ID: {saved_instance.id} ===")
            print(f"=== DEBUG: Expediente guardado: {saved_instance.expediente} ===")
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
    mem_medico_nombre = ''


    try:
        # Primero intentar obtener una existente
        receta = Recetas.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False


    except Recetas.DoesNotExist:
        # Si no existe, crear una nueva
        receta = Recetas(expediente=interno.numeroexpediente)
        receta.clinica = clinica_actual
        receta.medico = mem_user_no

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
            saved_instance.medico = mem_user_no  # Asegurar el expediente
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

      # 2. Buscar consejería existente o crear una nueva
    try:
        # Primero intentar obtener una existente
        historiaclinica = HistoriaClinica.objects.get(expediente=interno.numeroexpediente,clinica=clinica_actual)
        creado = False



        print(f"=== DEBUG: Plan existente encontrado - ID: {historiaclinica.id} ===")
        print(f"=== DEBUG: con expediente : {historiaclinica.expediente} ===")

    except HistoriaClinica.DoesNotExist:
        # Si no existe, crear una nueva
        historiaclinica = HistoriaClinica(expediente=interno.numeroexpediente)
        historiaclinica.medico = mem_user_no
        historiaclinica.clinica = clinica_actual
        historiaclinica.save()
        creado = True
        print(f"=== DEBUG: Nuevo plan creado - ID: {historiaclinica.id} ===")
        print(f"=== DEBUG: con expediente : {historiaclinica.expediente} ===")
    except HistoriaClinica.MultipleObjectsReturned:
        # Si hay múltiples, tomar el más reciente
        historiaclinica = HistoriaClinica.objects.filter(expediente=interno.numeroexpediente,clinica=clinica_actual).latest('id')
        creado = False
        print(f"=== DEBUG: Múltiples planes, tomando el más reciente - ID: {historiaclinica.id} ===")

    if request.method == 'POST':
        print("=== DEBUG: POST recibido ===")
        print(f"=== DEBUG: Datos POST: {request.POST} ===")  # Ver qué datos llegan
        historiaclinica.medico=mem_user_no
        historiaclinica.clinica=clinica_actual

        # Crear el formulario con los datos del POST y la instancia existente
        historiaclinicaf = HistoriaClinicaf(request.POST, instance=historiaclinica)

        print(f"Formulario válido: {historiaclinicaf.is_valid()}")

        if historiaclinicaf.is_valid():
            # FORZAR EL EXPEDIENTE ANTES DE GUARDAR
            saved_instance = historiaclinicaf.save(commit=False)
            saved_instance.expediente = interno.numeroexpediente  # Asegurar el expediente
            saved_instance.medico = mem_user_no  # Asegurar el expediente
            saved_instance.clinica = clinica_actual  # Asegurar el expediente

            # Asegurar que el médico sea el usuario actual - CORREGIDO
            if not saved_instance.medico:
                saved_instance.medico = mem_user_no
                saved_instance.clinica = clinica_actual

            saved_instance.save()

            print(f"=== DEBUG: Guardado exitoso - ID: {saved_instance.id} ===")
            print(f"=== DEBUG: Expediente guardado: {saved_instance.expediente} ===")
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
        request.session.flush()
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
    from mapp.models import ClinicaManager
    print("🔍 DEBUG MIDDLEWARE:")
    print(f"¿Tiene _request el manager?: {hasattr(ClinicaManager, '_request')}")
    if hasattr(ClinicaManager, '_request'):
        print(f"Clínica en sesión: {ClinicaManager._request.session.get('clinica_actual')}")
    else:
        print("❌ El manager NO tiene _request - el middleware no está funcionando")



    # Verificar que esté loggeado
    if 'clinica_actual' not in request.session:
        return redirect('login_clinica')

    # Aquí van tus vistas normales
    return render(request, 'MenuPrincipal.html')