# Generated by Django 3.1.3 on 2020-11-20 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0002_turno'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='nacimiento',
            field=models.DateField(default='2000-01-01', verbose_name='Fecha de Nacimiento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], default=('otro', 'Otro'), max_length=20),
            preserve_default=False,
        ),
    ]
