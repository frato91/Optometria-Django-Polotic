# Generated by Django 3.1.3 on 2020-11-28 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinica', '0005_turno_asistencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='asistencia',
            field=models.CharField(choices=[('-', ''), ('asistio', 'Asistió'), ('no_asistio', 'No Asistió')], default='-', max_length=20),
        ),
        migrations.CreateModel(
            name='HistorialMedico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=100)),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.paciente', verbose_name='Paciente')),
            ],
        ),
    ]