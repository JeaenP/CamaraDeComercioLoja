# Generated by Django 5.0 on 2023-12-06 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='description',
            new_name='cedula',
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='category',
            new_name='ciudad',
        ),
        migrations.RenameField(
            model_name='expense',
            old_name='date',
            new_name='fecha',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='owner',
        ),
        migrations.AddField(
            model_name='expense',
            name='nombres',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expense',
            name='telefono',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
