"""
URL configuration for ctrlinfo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from idlelib import run

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mapp.views import  primermenu,listaint, registro, datosgrales, grabadatosgrales,lusuarios,\
                        agregausuario,grabadatosusuario,editausuario,borrausuario,borrainterno,agregainterno,seleccionainterno,\
                        grabainterno,probar,consentimiento,einicial,assist,grabaeinicial,psicosis,sdevida,usodrogas,ansiedad,depresion,\
                        marcadores,riesgos,razones,valorizacion,\
                        listaSesiones,capturaSesion,capturaSesionGrupal,listaSesionesGrupales,planConsejeria,escanear_tarea,\
                        lista_tareas_escaneadas,eliminar_tarea,lista_archivos_word,imprimir_archivos_word,hojaAtencionPs,\
                        listaSesionesPS,capturaSesionPS,medicoInicial,emisionDerecetas,historiaClinica,validar_usuario,\
                        cerrar_sesion,imprime_contrato,imprime_solicitud,imprime_aviso,login_clinica,dashboard,salidas,\
                        seguimiento,listaSesionesS,capturaSesionS,reporte_internos,captura_pagos,guardar_pago,imprimir_recibo_pdf,\
                        lista_recibos,cancelar_recibo,menu_reportes,reporte_cuotas_por_recibir,reporte_cuotas_recibidas




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_clinica, name='login_clinica'),
    path('dashboard/', dashboard, name='dashboard'),
    path('menuprincipal/', primermenu, name='Menu principal'),
    path('listaint/',listaint,name='listaint'),
    path('agregainterno/',agregainterno,name='agregainterno'),
    path('selecciona/<int:id>/', seleccionainterno, name='seleccionainterno'),
    path('borrainterno/<int:id>/',borrainterno,name='borrainterno'),
    path('grabainterno/<int:id>/', grabainterno, name='grabainterno'),
    path('registro/',registro,name='registro'),
    path('datosgrales/',datosgrales,name='datosgrales'),
    path('grabadatosgrales/',grabadatosgrales,name='grabadatosgrales'),
    path('lusuarios/',lusuarios,name='lusuarios'),
    path('agregausuario/',agregausuario,name='agregausuario'),
    path('grabadatosusuario/<int:id>/',grabadatosusuario,name='grabadatosusuario'),
    path('editausuario/<int:id>/',editausuario,name='editausuario'),
    path('borrausuario/<int:id>/',borrausuario,name='borrausuario'),
    path('probar/', probar, name='probar'),
    path('consentimiento/<int:id>/',consentimiento,name='consentimiento'),
    path('einicial/<int:id>/',einicial,name='einicial'),
    path('grabaeinicial/<int:id>/',grabaeinicial,name='grabaeinicial'),
    path('assist/<int:id>/', assist, name='assist'),
    path('psicosis/<int:id>/', psicosis, name='psicosis'),
    path('sdevida/<int:id>/', sdevida, name='sdevida'),
    path('usodrogas/<int:id>/', usodrogas, name='usodrogas'),
    path('ansiedad/<int:id>/', ansiedad, name='ansiedad'),
    path('depresion/<int:id>/', depresion, name='depresion'),
    path('marcadores/<int:id>/', marcadores, name='marcadores'),
    path('riesgos/<int:id>/', riesgos, name='riesgos'),
    path('razones/<int:id>/', razones, name='razones'),
    path('valorizacion/<int:id>/', valorizacion, name='valorizacion'),
    path('listaSesiones/<str:tipo_sesion>/<str:id>/', listaSesiones, name='listaSesiones'),
    path('listaSesionesPS/<str:id>/', listaSesionesPS, name='listaSesionesPS'),
    path('listaSesionesS/<str:id>/', listaSesionesS, name='listaSesionesS'),
    path('capturaSesion/<str:tipo_sesion>/<str:accion>/<str:id>/', capturaSesion, name='capturaSesion'),
    path('capturaSesionPS/<str:accion>/<str:id>/', capturaSesionPS, name='capturaSesionPS'),
    path('capturaSesionS/<str:accion>/<str:id>/', capturaSesionS, name='capturaSesionS'),
    path('capturaSesion/<str:tipo_sesion>/<str:accion>/<str:id>/<int:no_sesion>/', capturaSesion, name='capturaSesion_con_id'),
    path('capturaSesionPS/<str:accion>/<str:id>/<int:no_sesion>/', capturaSesionPS, name='capturaSesionPS_con_id'),
    path('capturaSesionS/<str:accion>/<str:id>/<int:no_sesion>/', capturaSesionS, name='capturaSesionS_con_id'),
    path('sesiones-grupales/', listaSesionesGrupales, name='listaSesionesGrupales'),
    path('sesion-grupal/<str:tipo_sesion>/<str:accion>/', capturaSesionGrupal, name='capturaSesionGrupal'),
    path('sesion-grupal/<str:tipo_sesion>/<str:accion>/<int:no_sesion>/', capturaSesionGrupal, name='capturaSesionGrupal_con_id'),
    path('planConsejeria/<int:id>/', planConsejeria, name='planConsejeria'),
    path('hojaAtencionPs/<str:id>/', hojaAtencionPs, name='hojaAtencionPs'),
    path('medicoInicial/<int:id>/', medicoInicial, name='medicoInicial'),
    path('emisionDerecetas/<int:id>/', emisionDerecetas, name='emisionDerecetas'),
    path('historiaClinica/<int:id>/', historiaClinica, name='historiaClinica'),
    path('escanear-tarea/', escanear_tarea, name='escanear_tarea'),
    path('lista-tareas/', lista_tareas_escaneadas, name='lista_tareas_escaneadas'),
    path('eliminar-tarea/<int:tarea_id>/', eliminar_tarea, name='eliminar_tarea'),
    path('imprimir-word/', lista_archivos_word, name='lista_archivos_word'),
    path('imprimir-word/enviar/', imprimir_archivos_word, name='imprimir_archivos_word'),
    path('validar-usuario/', validar_usuario, name='validar_usuario'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('contrato-completo/<int:id>', imprime_contrato, name='imprime_contrato'),
    path('imprime_solicitud/<int:id>', imprime_solicitud, name='imprime_solicitud'),
    path('imprime_aviso/<int:id>', imprime_aviso, name='imprime_aviso'),
    path('salidas/<int:id>', salidas, name='salidas'),
    path('seguimiento/<int:id>', seguimiento, name='seguimiento'),
    path('reporte_internos/', reporte_internos, name='reporte_internos'),
    path('captura_pagos/', captura_pagos, name='captura_pagos'),
    path('guardar_pago/<int:id>', guardar_pago, name='guardar_pago'),
    path('imprimir-recibo/<int:id_recibo>', imprimir_recibo_pdf, name='imprimir_recibo'),
    path('recibos/consultar/', lista_recibos, name='lista_recibos'),

    # 2. Acción de Cancelar (Oculta, se llama desde el botón)
    path('recibos/cancelar/<int:id_recibo>/', cancelar_recibo, name='cancelar_recibo'),

    # 3. Tu vista de impresión ya existe (asegúrate que esté así)
    path('imprimir-recibo/<int:id_recibo>/', imprimir_recibo_pdf, name='imprimir_recibo'),
    path('reportes/menu/', menu_reportes, name='menu_reportes'),

    # Generadores de PDF
    path('reportes/pdf/recibidas/', reporte_cuotas_recibidas, name='rep_recibidas'),
    path('reportes/pdf/por-recibir/', reporte_cuotas_por_recibir, name='rep_por_recibir'),
]






if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
