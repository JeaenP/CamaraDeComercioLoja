# Generated by Django 5.0.1 on 2024-01-17 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0025_remove_expense_latitud_comercial_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='latitud_comercial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='latitud_domicilio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='longitud_comercial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='longitud_domicilio',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
