from django.db import models

# Create your models here.
class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    lente = models.BooleanField(verbose_name='Es un lente?')
    distancia_choices = (
        ('-', ''),
        ('lejos', 'Lejos'),
        ('cerca','Cerca'),
    )
    distancia = models.CharField(max_length=20, choices=distancia_choices, default='-')
    lado_choices = (
        ('-', ''),
        ('izquierda', 'Izquierda'),
        ('derecha','Derecha'),
    )
    lado = models.CharField(max_length=20, choices=lado_choices, default='-')
    armazon = models.BooleanField(verbose_name='Incluye armazón?')
    precio = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre}"


class Pedido(models.Model):
    creation = models.DateTimeField(verbose_name='Fecha de Creación', auto_now=False, auto_now_add=True)
    update = models.DateTimeField(verbose_name='Fecha de Modificación', auto_now=True)
    paciente = models.ForeignKey("clinica.Paciente", verbose_name="Paciente", on_delete=models.CASCADE)
    vendedor = models.ForeignKey("auth.User", verbose_name="Vendedor", on_delete=models.PROTECT)
    estado_choices = (
        ('pendiente', 'Pendiente'),
        ('pedido','Pedido'),
        ('taller','Taller'),
        ('finalizado','Finalizado'),
    )
    estado = models.CharField(max_length=20, choices=estado_choices, default='pendiente')
    pago_choices = (
        ('Tarjeta de Credito', 'Tarjeta de Credito'),
        ('Billetera Virtual', 'Billetera Virtual'),
        ('Efectivo', 'Efectivo'),
        ('Debito', 'Debito'),
    )
    pago = models.CharField(max_length=20, choices=pago_choices, default='Efectivo')

    def precio(self):
        productos = PedidoProducto.objects.filter(pedido=self)
        precio = 0
        for producto in productos:
            precio += producto.producto.precio * producto.cantidad
        return precio

    def cantidad(self):
        productos = PedidoProducto.objects.filter(pedido=self)
        cantidad = 0
        for producto in productos:
            cantidad += producto.cantidad
        return cantidad

    def __str__(self):
        return f"{self.id} | {self.paciente}"


class PedidoProducto(models.Model):

    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad", default=1)

    def subtotal(self):
        precio = self.cantidad * self.producto.precio
        return precio

    def __str__(self):
        return f"{self.pedido} | {self.producto}:{self.cantidad}"
