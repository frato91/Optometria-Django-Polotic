from django.contrib import admin
from venta import models

# Register your models here.

admin.site.register(models.Productos)
admin.site.register(models.Pedido)
admin.site.register(models.PedidoProducto)