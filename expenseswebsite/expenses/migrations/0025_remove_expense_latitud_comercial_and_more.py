# Generated by Django 5.0.1 on 2024-01-17 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0024_pago_mes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='latitud_comercial',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='latitud_domicilio',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='longitud_comercial',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='longitud_domicilio',
        ),
    ]
