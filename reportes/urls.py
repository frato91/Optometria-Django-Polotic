from django.contrib import admin
from django.urls import path, include

from reportes import views


urlpatterns = [
    path('', views.reportes, name='reportes'),
    path('<int:reporte>/', views.reportes_opciones, name='reportes_opciones'),
]