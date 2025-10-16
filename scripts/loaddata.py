import os
import django
import subprocess
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrlinfo.settings')
django.setup()

from django.core.management import call_command


def cargar_datos():
    try:
        print("🔧 Intentando cargar datos desde datos.json...")

        # Verificar si el archivo existe
        if not os.path.exists('datos.json'):
            print("❌ Archivo datos.json no encontrado")
            return

        # Cargar datos
        call_command('loaddata', 'datos.json')
        print('✅ Datos cargados exitosamente desde datos.json')

    except Exception as e:
        print(f'❌ Error cargando datos: {e}')


# Ejecutar automáticamente
if __name__ == '__main__':
    cargar_datos()