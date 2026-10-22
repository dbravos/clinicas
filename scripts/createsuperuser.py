import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrlinfo.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@clinicas.com', 'clinicas123')
    print('✅ Superusuario creado: admin / clinicas123')
else:
    print('⚠️  El superusuario admin ya existe')