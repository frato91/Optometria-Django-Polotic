from django.contrib import admin
from django.urls import path, include

from clinica import views


urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('pacientes/<int:id_p>/', views.paciente_detail, name='paciente_detail'),
    path('pacientes/add/', views.paciente_add, name='paciente_add'),
    path('pacientes/edit/<int:id_p>/', views.paciente_edit, name='paciente_edit'),
    path('pacientes/del/<int:id_p>/', views.paciente_del, name='paciente_del'),
    path('pacientes/<int:id_p>/turno/', views.turnos_add, name='turnos_add'),
    path('pacientes/<int:id_p>/turno/<int:id_turno>', views.turnos_edit, name='turnos_edit'),
    path('pacientes/<int:id_p>/turno/<int:id_turno>/del', views.turnos_del, name='turnos_del'),
    path('turnos/', views.turnos, name='turnos'),
    path('pacientes/<int:id_p>/historial_medico/', views.historial_medico_add, name='historial_medico_add'),
    path('pacientes/<int:id_p>/historial_medico/<int:id_hm>/', views.historial_medico_detail, name='historial_medico_detail'),
]