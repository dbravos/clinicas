from django.db import models

class Lead(models.Model):

    ESTATUS_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('contactado', 'Contactado'),
        ('demo', 'Demo Agendada'),
        ('cerrado', 'Cliente Cerrado'),
    ]

    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    clinica = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    estatus = models.CharField(
        max_length=20,
        choices=ESTATUS_CHOICES,

        default='nuevo'
    )

    notas = models.TextField(blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.clinica}"