import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrlinfo.settings')
django.setup()

from django.core.management import call_command


# En scripts/loaddata.py, mejor crear datos programáticamente:
def cargar_datos():
    from django.contrib.auth.models import User
    from mapp.models import Clinicas, Usuarios

    # Crear superusuario
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@clinicas.com', 'admin123')

    from mapp.models import Clinicas, Usuarios, DatosGrales

    if not Clinicas.objects.exists():
       Clinicas.objects.create(
        clinica='VIVE',
        nombre='VIVE CONCIENTE, A.C.',
        password='123456',
        numeroDeInternos=0
    )
    if not DatosGrales.objects.exists():
       DatosGrales.objects.create(
        clinica='VIVE',
        nombre='VIVE CONCIENTE, A.C.',
        password='123456',
    )

    if not Usuarios.objects.exists():
       Usuarios.objects.create(
        usuario=1,
        nombre='superUser',
        permisos='admin',
        password='123456',
        clinica='VIVE'

    )

    print('✅ ¡Listo!')


          

    print("✅ Datos básicos creados")

