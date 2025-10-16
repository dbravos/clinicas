import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrlinfo.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
import json


def cargar_datos():
    try:
        print("🔧 Iniciando carga de datos...")

        # VERIFICAR SI HAY MÁS USUARIOS BESIDES EL SUPERUSUARIO
        total_usuarios = User.objects.count()
        print(f"👥 Usuarios en BD: {total_usuarios}")

        # Si solo existe el superusuario admin, cargar datos
        if total_usuarios <= 1:  # Solo admin o ninguno
            print("📦 Cargando datos desde datos.json...")

            if not os.path.exists('datos.json'):
                print("❌ Archivo datos.json no encontrado")
                return

            # Cargar datos
            call_command('loaddata', 'datos.json')
            print('✅ Datos de prueba cargados exitosamente!')
        else:
            print("⚠️  Ya existen datos de usuarios. Saltando carga.")

    except Exception as e:
        print(f'❌ Error cargando datos: {e}')
        import traceback
        print(traceback.format_exc())


if __name__ == '__main__':
    cargar_datos()