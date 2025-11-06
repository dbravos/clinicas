import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrlinfo.settings')
django.setup()

from django.core.management import call_command


# En scripts/loaddata.py, mejor crear datos programáticamente:
def cargar_datos():
    from mapp.models import Clinicas, DatosGrales, Usuarios

    print("🔧 Iniciando carga de datos...")

    try:
        # 1. ELIMINAR registros existentes
        print("🗑️  Limpiando datos existentes...")
        Usuarios.objects.all().delete()
        DatosGrales.objects.all().delete()
        Clinicas.objects.all().delete()
        print("✅ Datos anteriores eliminados")

        # 2. CREAR clínica principal
        print("🏥 Creando clínica VIVE...")
        clinica_vive = Clinicas.objects.create(
            clinica="DEMO",
            nombre="Clinica De Demostracion",
            password="demo",
            numeroDeInternos=0
        )
        print("✅ Clínica VIVE creada")

        # 3. CREAR datos generales
        print("📋 Creando datos generales...")
        DatosGrales.objects.create(
            nombre="Clinica De Demostracion",
            responsable="",
            cedula="",
            cargo="",
            clinica="DEMO",
            password="demo",
            expediente=None,
            recibo=0,
            receta=0,
            recibootros=0,
            sesiong=0
        )
        print("✅ Datos generales creados")

        # 4. CREAR usuario superuser
        print("👤 Creando usuario superUser...")
        Usuarios.objects.create(
            usuario=1,
            nombre="superUser",
            cargo="",
            permisos="admin",
            password="123456",
            cedula="",
            expedidapor="",
            clinica="DEMO"
        )
        print("✅ Usuario superUser creado")

        print("🎉 Carga de datos completada exitosamente")

    except Exception as e:
        print(f"❌ Error en carga de datos: {e}")