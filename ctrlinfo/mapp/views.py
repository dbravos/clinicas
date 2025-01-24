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

def editainterno(request,id):
    interno = get_object_or_404(Internos, pk=id)
    internof = Internosf(instance=interno)
    intresponsablef=IntResponsablef(instance=interno)
    intdependientesf=IntDependientesf(instance=interno)
    intprovienef=IntProvienef(instance=interno)
    if request.method == "POST":
        return consentimiento(interno)

    return render(request, 'internosnw.html', {'interno':interno,'internof':internof, 'intresponsablef':intresponsablef, 'intdependientesf':intdependientesf,'intprovienef':intprovienef })

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

def consentimiento(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="consentimiento.pdf"'
    interno=Internos.objects
    # Crear un canvas de ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Agregar un título al reporte
    p.drawString(100, height - 100, "Consentimiento Informado")
    # Obtener la lista de internos
    # internos=Internos.objects.all()
    logo="c:/viveprg/logo.jpg"
    # Agregar los datos de los internos al reporte
    p.drawImage(logo,10,680,width=120,height=100)
    y = height - 150
   # for interno in internos:
    p.drawString(100, y, f"{interno.numeroexpediente} - {interno.nombrecompleto}")
    y -= 20

    # Finalizar el PDF
    p.showPage()
    p.save()

    return response
