from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('leads/', views.lista_leads, name='lista_leads'),
]