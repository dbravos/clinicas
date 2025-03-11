from django.db.models import Q
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from mapp.models import Internos,Usuarios,DatosGrales
from .formas import DatosGralesf,Usuariosf,Internosf,IntResponsablef,IntDependientesf,IntProvienef
from django.http import request, Http404, HttpResponse
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import win32print
import win32api
import os

# Create your views here.

def primermenu(request):
    return render(request,'MenuPrincipal.html')

def probar(request):
    return render(request,'agregar.html')

def listaint(request):
    internos = Internos.objects.raw('SELECT * FROM mapp_internos ORDER BY numeroexpediente')
    return render(request, 'listar.html', {'internos': internos})

def agregainterno(request):
    interno = Internos()
    interno.numeroexpediente='0'
    interno.save()
    interno.numeroexpediente=str(interno.pk)
    interno.save()
    internof=Internosf(instance=interno)
    intresponsablef = IntResponsablef(instance=interno)
    intdependientesf = IntDependientesf(instance=interno)
    intprovienef = IntProvienef(instance=interno)

    return render(request, 'internos.html', {'interno':interno,'internof':internof, 'intresponsablef':intresponsablef, 'intdependientesf':intdependientesf,'intprovienef':intprovienef})

def seleccionainterno(request,id):
    interno = get_object_or_404(Internos, pk=id)
    opcion = request.GET.get('opcion', None)
    internof = Internosf(instance=interno)
    intresponsablef=IntResponsablef(instance=interno)
    intdependientesf=IntDependientesf(instance=interno)
    intprovienef=IntProvienef(instance=interno)
    if opcion=="editar":
       return render(request, 'internosnw.html', {'interno':interno,'internof':internof, 'intresponsablef':intresponsablef, 'intdependientesf':intdependientesf,'intprovienef':intprovienef })
    else:
       return render(request, 'dgenerales.html', {'interno':interno})

def borrainterno(request,id):
    interno = get_object_or_404(Internos, pk=id)
    interno.delete()
    messages.success(request, 'Interno de expediente  #' + str(interno.id)+' borrado')
    internos = Internos.objects.raw('SELECT * FROM mapp_internos ORDER BY numeroexpediente')
    return render(request, 'listar.html', {'internos': internos})

def grabainterno(request,id):
    interno = Internos.objects.get(pk=id)
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

    internos = Internos.objects.raw('SELECT * FROM mapp_internos ORDER BY numeroexpediente')
    return render(request, 'listar.html', {'internos': internos})

def registro(request):
    return render(request,'registro.html')

def datosgrales(request):
    try :
       datosgrales=DatosGrales.objects.first()
       datosgralesf=DatosGralesf(instance=datosgrales)
       return render(request, 'datosgrales.html', {'datosgrales': datosgrales, 'datosgralesf': datosgralesf})
    except:
        datosgrales=DatosGrales()
        datosgrales.nombre='nombre'
        datosgrales.calleynumero='calle y numero'
        datosgrales.colonia='colonia'
        datosgrales.ciudad='ciudad'
        datosgrales.estado='BC'
        datosgrales.telefono='telefono'
        datosgrales.sitioweb='sitio web'
        datosgrales.correoelectronico='correo electrinco'
        datosgrales.rfc='rfc'
        datosgrales.cp='cp'
        datosgrales.expediente=1
        datosgrales.recibo=1
        datosgrales.receta=1
        datosgrales.recibootros=1
        datosgrales.sesiong=1
        datosgrales.responsable='responsable'
        datosgrales.cedula='cedula'
        datosgrales.cargo='cargo'
        datosgrales.save()
        datosgralesf=DatosGrales.objects.first()
    return render(request,'datosgrales.html',{'datosgrales':datosgrales,'datosgralesf':datosgralesf})

def grabadatosgrales(request):
    datosgrales=DatosGrales.objects.first()
    datosgralesf=DatosGralesf(request.POST,instance=datosgrales)
    if datosgralesf.is_valid():
        datosgralesf.save()
        messages.success(request,'Actualizacion exitosa!!')
    else:
        messages.error(request,'Algo paso que no se pudo acualizar')
    return render(request,'index.html')



def lusuarios(request):
    usuarios = Usuarios.objects.raw('SELECT * FROM mapp_usuarios ORDER BY nombre')
    return render(request, 'lusuarios.html', {'usuarios': usuarios})

def agregausuario(request):
    usuario = Usuarios()
    usuario.usuario=0
    usuario.save()
    usuario.usuario=usuario.pk
    usuario.save()
    usuariof=Usuariosf(instance=usuario)
    return render(request, 'usuarios.html', {'usuario':usuario,'usuariof':usuariof})

def grabadatosusuario(request,id):
    usuario = Usuarios.objects.get(pk=id)
    usuariof= Usuariosf(request.POST,instance=usuario)
    if usuariof.is_valid():
        usuariof.save()
        messages.success(request,'Actualizacion existosa '+str(usuario.usuario))
    else:
        messages.error(request,'No se Actualizo ' + str(id))

    usuarios = Usuarios.objects.raw('SELECT * FROM mapp_usuarios ORDER BY nombre')
    return render(request, 'lusuarios.html', {'usuarios': usuarios})

def editausuario(request,id):
    usuario = get_object_or_404(Usuarios, pk=id)
    usuariof = Usuariosf(instance=usuario)
    return render(request, 'usuarios.html', {'usuario':usuario,'usuariof':usuariof})

def borrausuario(request,id):
    usuario = get_object_or_404(Usuarios, pk=id)
    usuario.delete()
    messages.success(request, 'Usuario #' + str(usuario.usuario)+' borrado')
    usuarios = Usuarios.objects.raw('SELECT * FROM mapp_usuarios ORDER BY nombre')
    return render(request, 'lusuarios.html', {'usuarios': usuarios})

def consentimiento(request,id):
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


    logo="c:/viveprg/logo.jpg"

    p.drawImage(logo,10,680,width=120,height=100)
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

