# Generated by Django 5.0 on 2023-12-20 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0015_remove_expense_cedula_remove_expense_ciudad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='cedula_ruc',
            field=models.TextField(blank=True, max_length=15, null=True),
        ),
    ]