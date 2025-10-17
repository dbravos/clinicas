import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrlinfo.settings')
django.setup()

from django.core.management import call_command


def cargar_datos():
    try:
        print("🔧 Iniciando carga de datos...")

        if not os.path.exists('datos.json'):
            print("❌ Archivo datos.json no encontrado")
            return

        # Especificar codificación UTF-8 explícitamente
        call_command('loaddata', 'datos.json', verbosity=1)
        print('✅ Datos cargados exitosamente!')

    except Exception as e:
        print(f'❌ Error cargando datos: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    cargar_datos()