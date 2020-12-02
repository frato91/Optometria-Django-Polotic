from django import forms
from .models import Rol, Paciente

class form_pacientes(forms.Form):
    nombre = forms.CharField(max_length=30)
    apellido = forms.CharField(max_length=30)
    dni = forms.IntegerField()
    telefono = forms.IntegerField()
    user_medicos=Rol.objects.filter(rol='profecional_medico')
    choices = []
    for user_medico in user_medicos:
        a = (user_medico.user.id, f"{user_medico.user.last_name.upper()}, {user_medico.user.first_name}")
        choices.append(a)
    tuple(choices)
    medico = forms.ChoiceField(choices=choices, label='Médico')

class form_turnos(forms.Form):
    date = forms.DateField(label='Facha del Turno')
    choices = []
    for hora in range(8,19):
        a = (f"{str(hora).zfill(2)}:00", f"{str(hora).zfill(2)}:00")
        choices.append(a)
    tuple(choices)
    hour = forms.ChoiceField(choices=choices, label='Horario')

class form_asistencia(forms.Form):
    choices = (
        ('-',''),
        ('asistio','Asistió'),
        ('no_asistio','No Asistió'),
    )
    asistencia = forms.ChoiceField(choices=choices, label='Asistencia')

class form_historial_medico(forms.Form):
    asunto = forms.CharField(max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea)