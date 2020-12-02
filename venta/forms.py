from django import forms
from clinica.models import Paciente
from .models import Productos

class form_producto(forms.Form):
    nombre = forms.CharField(max_length=50, label='Producto')
    precio = forms.IntegerField(min_value=0)
    lente = forms.BooleanField(required=False)
    distancia_choices = (
        ('-',''),
        ('lejos','Lejos'),
        ('cerca','Cerca'),
    )
    distancia = forms.ChoiceField(choices=distancia_choices, label='Distancia')
    lado_choices = (
        ('-',''),
        ('izquierda','Izquierda'),
        ('derecha','Derecha'),
    )
    lado = forms.ChoiceField(choices=lado_choices, label='Lado')
    armazon = forms.BooleanField(required=False)

class form_pedido(forms.Form):
    clientes=Paciente.objects.order_by('apellido')
    choices = []
    for cliente in clientes:
        a = (cliente.id, f"{cliente.apellido.upper()}, {cliente.nombre} ({str(cliente.dni)[-3:]})")
        choices.append(a)
    tuple(choices)
    cliente = forms.ChoiceField(choices=choices, label='Cliente')
    choices = (
        ('Efectivo', 'Efectivo'),
        ('Debito', 'Debito'),
        ('Tarjeta de Credito', 'Tarjeta de Credito'),
        ('Billetera Virtual', 'Billetera Virtual'),  
    )
    pago = forms.ChoiceField(choices=choices, label='Pago',)


class form_pedido_estado(forms.Form):
    choices = (
        ('pendiente', 'Pendiente'),
        ('pedido','Pedido'),
        ('taller','Taller'),
    )
    estado = forms.ChoiceField(choices=choices, label='Estado')

class form_estado_taller(forms.Form):
    choices = (
        ('taller','Taller'),
        ('finalizado','Finalizado'),
    )
    estado = forms.ChoiceField(choices=choices, label='Estado')

class form_item_add(forms.Form):
    productos= Productos.objects.order_by('nombre')
    choices = []
    for producto in productos:
        if producto.lente == True:
            if producto.armazon == True:
                a = (producto.id, f"{producto.nombre} | {producto.distancia.title()} | {producto.lado.title()} | Con Armazón")
            else:
                a = (producto.id, f"{producto.nombre} | {producto.distancia.title()} | {producto.lado.title()} | Sin Armazón")
        else:
            a = (producto.id, f"{producto.nombre}")
        choices.append(a)
    tuple(choices)
    producto = forms.ChoiceField(choices=choices, label='Producto', required=False)
    cantidad = forms.IntegerField(min_value=1)