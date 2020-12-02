from django.db import models
from django.contrib.auth.models import User

class Rol (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol_choices = (
        ('secretaria', 'Secretaria'),
        ('profecional_medico', 'Profecional Medico'),
        ('ventas','Ventas'),
        ('taller', 'Taller'),
        ('gerencia', 'Gerencia'),
    )
    rol = models.CharField(max_length=20, choices=rol_choices)

    class Meta:
        verbose_name = ("Rol")
        verbose_name_plural = ("Roles")

    def __str__(self):
        return self.user.username + ' | ' + self.rol
