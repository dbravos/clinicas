# Generated by Django 4.2.5 on 2025-03-27 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0008_alter_internos_numeroexpediente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='einicial',
            name='id',
        ),
        migrations.AlterField(
            model_name='einicial',
            name='expediente',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='No.Expediente'),
        ),
    ]
