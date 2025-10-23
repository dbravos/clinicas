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
                        grabainterno,probar,consentimiento,einicial,assist,grabaeinicial,grabalo,psicosis,assist_cfg,\
                        psicosis_cfg,sdevida_cfg,sdevida,usodrogas,usodrogas_cfg,ansiedad,ansiedad_cfg,depresion,depresion_cfg,\
                        marcadores_cfg,marcadores,riesgos,riesgos_cfg,razones,razones_cfg,valorizacion,valorizacion_cfg,\
                        listaSesiones,capturaSesion,capturaSesionGrupal,listaSesionesGrupales,planConsejeria,escanear_tarea,\
                        lista_tareas_escaneadas,eliminar_tarea,lista_archivos_word,imprimir_archivos_word,hojaAtencionPs,\
                        listaSesionesPS,capturaSesionPS,medicoInicial,emisionDerecetas,historiaClinica,validar_usuario,\
                        cerrar_sesion,imprime_contrato,imprime_solicitud,imprime_aviso,login_clinica,dashboard



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
    path('graba-assist/<int:id>/', assist_cfg, name='graba-assist'),
    path('graba-psicosis/<int:id>/', psicosis_cfg, name='graba-psicosis'),
    path('psicosis/<int:id>/', psicosis, name='psicosis'),
    path('sdevida/<int:id>/', sdevida, name='sdevida'),
    path('graba-sdevida/<int:id>/', sdevida_cfg, name='graba-sdevida'),
    path('usodrogas/<int:id>/', usodrogas, name='usodrogas'),
    path('graba-usodrogas/<int:id>/', usodrogas_cfg, name='graba-usodrogas'),
    path('ansiedad/<int:id>/', ansiedad, name='ansiedad'),
    path('graba-ansiedad/<int:id>/', ansiedad_cfg, name='graba-ansiedad'),
    path('depresion/<int:id>/', depresion, name='depresion'),
    path('graba-depresion/<int:id>/', depresion_cfg, name='graba-depresion'),
    path('marcadores/<int:id>/', marcadores, name='marcadores'),
    path('graba-marcadores/<int:id>/', marcadores_cfg, name='graba-marcadores'),
    path('riesgos/<int:id>/', riesgos, name='riesgos'),
    path('graba-riesgos/<int:id>/', riesgos_cfg, name='graba-riesgos'),
    path('razones/<int:id>/', razones, name='razones'),
    path('graba-razones/<int:id>/', razones_cfg, name='graba-razones'),
    path('valorizacion/<int:id>/', valorizacion, name='valorizacion'),
    path('graba-valorizacion/<int:id>/', valorizacion_cfg, name='graba-valorizacion'),
    path('listaSesiones/<str:tipo_sesion>/<int:id>/', listaSesiones, name='listaSesiones'),
    path('listaSesionesPS/<int:id>/', listaSesionesPS, name='listaSesionesPS'),
    path('capturaSesion/<str:tipo_sesion>/<str:accion>/<int:id>/', capturaSesion, name='capturaSesion'),
    path('capturaSesionPS/<str:accion>/<int:id>/', capturaSesionPS, name='capturaSesionPS'),
    path('capturaSesion/<str:tipo_sesion>/<str:accion>/<int:id>/<int:no_sesion>/', capturaSesion, name='capturaSesion_con_id'),
    path('capturaSesionPS/<str:accion>/<int:id>/<int:no_sesion>/', capturaSesionPS, name='capturaSesionPS_con_id'),
    path('sesiones-grupales/', listaSesionesGrupales, name='listaSesionesGrupales'),
    path('sesion-grupal/<str:tipo_sesion>/<str:accion>/', capturaSesionGrupal, name='capturaSesionGrupal'),
    path('sesion-grupal/<str:tipo_sesion>/<str:accion>/<int:no_sesion>/', capturaSesionGrupal, name='capturaSesionGrupal_con_id'),
    path('planConsejeria/<int:id>/', planConsejeria, name='planConsejeria'),
    path('hojaAtencionPs/<int:id>/', hojaAtencionPs, name='hojaAtencionPs'),
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

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
