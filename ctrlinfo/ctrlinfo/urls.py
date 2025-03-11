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
from idlelib import run

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mapp.views import  primermenu,listaint, registro, datosgrales, grabadatosgrales,lusuarios,\
                        agregausuario,grabadatosusuario,editausuario,borrausuario,borrainterno,agregainterno,seleccionainterno,\
                        grabainterno,probar,consentimiento

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', primermenu, name='Menu principal'),
    path('menuprincipal/', primermenu, name='Menu principal'),
    path('listaint/',listaint,name='listaint'),
    path('agregaint/',agregainterno,name='agregainterno'),
    path('selecciona/<int:id>', seleccionainterno, name='seleccionainterno'),
    path('borrainterno/<int:id>',borrainterno,name='borrainterno'),
    path('grabainterno/<int:id>', grabainterno, name='grabainterno'),
    path('registro/',registro,name='registro'),
    path('datosgrales/',datosgrales,name='datosgrales'),
    path('grabadatosgrales/',grabadatosgrales,name='grabadatosgrales'),
    path('lusuarios/',lusuarios,name='lusuarios'),
    path('agregausuario/',agregausuario,name='agregausuario'),
    path('grabadatosusuario/<int:id>',grabadatosusuario,name='grabadatosusuario'),
    path('editausuario/<int:id>',editausuario,name='editausuario'),
    path('borrausuario/<int:id>',borrausuario,name='borrausuario'),
    path('probar/', probar, name='probar'),
    path('consentimiento/<int:id>',consentimiento,name='consentimiento')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
