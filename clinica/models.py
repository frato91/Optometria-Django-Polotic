from django.db import models
from usuarios.models import Rol
from django.contrib.auth.models import User

# Create your models here.

#Pacientes
#asignado a un medico
class Paciente (models.Model):

    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.IntegerField(verbose_name='DNI')
    telefono = models.BigIntegerField(verbose_name='Teléfono')
    medico = models.ForeignKey("auth.User", verbose_name="Medico Asignado", on_delete=models.PROTECT)

    class Meta:
        verbose_name = ("Paciente")
        verbose_name_plural = ("pacientes")

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

#Turnos
class Turno (models.Model):
    paciente = models.ForeignKey("clinica.Paciente", verbose_name="Paciente", on_delete=models.CASCADE)
    creation = models.DateTimeField(verbose_name='Fecha de Creación', auto_now=False, auto_now_add=True)
    date = models.DateTimeField(verbose_name='Fecha del Turno', auto_now=False, auto_now_add=False)
    medico = models.ForeignKey("auth.User", verbose_name="Medico", on_delete=models.PROTECT)
    asistencia_choices = (
        ('-', ''),
        ('asistio', 'Asistió'),
        ('no_asistio','No Asistió'),
    )
    asistencia = models.CharField(max_length=20, choices=asistencia_choices, default='-')

    class Meta:
        verbose_name = ("Turno")
        verbose_name_plural = ("Turnos")

    def __str__(self):
        return f"{self.paciente.apellido} {self.paciente.nombre} | {self.date}"

#historial medico
#relacionado a pacientes
class HistorialMedico(models.Model):
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name='Descripción')
    creation = models.DateTimeField(verbose_name='Fecha de Creación', auto_now=False, auto_now_add=True)
    paciente = models.ForeignKey("clinica.Paciente", verbose_name="Paciente", on_delete=models.CASCADE)
    medico = models.ForeignKey("auth.User", verbose_name="Medico", on_delete=models.PROTECT)
