# Generated by Django 4.2.5 on 2024-05-29 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0005_alter_internos_porcualingresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internos',
            name='calleynumero',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='Domicilio actual'),
        ),
        migrations.AlterField(
            model_name='internos',
            name='ciudad',
            field=models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Ciudad actual'),
        ),
        migrations.AlterField(
            model_name='internos',
            name='colonia',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='Colonia actual'),
        ),
        migrations.AlterField(
            model_name='internos',
            name='estado',
            field=models.CharField(blank=True, default='', max_length=2, null=True, verbose_name='Estado actual'),
        ),
        migrations.AlterField(
            model_name='internos',
            name='estadonac',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Estado de nacimiento'),
        ),
        migrations.AlterField(
            model_name='internos',
            name='pais',
            field=models.CharField(blank=True, default='', max_length=2, null=True, verbose_name='Pais actual'),
        ),
        migrations.AlterField(
            model_name='internos',
            name='paisnac',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Pais de nacimiento'),
        ),
        migrations.AlterField(
            model_name='internos',
            name='porcualingresa',
            field=models.CharField(blank=True, choices=[('A', 'Alcohol'), ('B', 'Anfetaminas'), ('C', 'Secantes'), ('D', 'Marihuana'), ('E', 'Rohypnol'), ('F', 'Analgesicos'), ('G', 'Disolventes'), ('H', 'Cocaina'), ('I', 'Opcio'), ('J', 'Cristal')], default='', max_length=1, null=True, verbose_name='Por que sustancia ingresa'),
        ),
    ]
