# Generated by Django 5.0 on 2023-12-18 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0011_alter_expense_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='cedula',
            field=models.TextField(unique=True),
        ),
    ]