from django.contrib import admin
from .models import Paciente, Turno,HistorialMedico

# Register your models here.
admin.site.register(Paciente) # tiene el problema de que aparecen todos los usuarios y no solo los medicos
admin.site.register(Turno)
admin.site.register(HistorialMedico)