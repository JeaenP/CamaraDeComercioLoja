# Generated by Django 5.0.1 on 2024-01-10 21:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0021_aseguradora_comite_estado_estadocivil_genero_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateField()),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.expense')),
            ],
        ),
    ]
