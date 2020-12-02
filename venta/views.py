from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from venta import models 
from clinica.models import Paciente
from venta.forms import form_producto, form_pedido, form_pedido_estado, form_item_add, form_estado_taller
#from .forms import form_pacientes

# Create your views here.

@login_required
def productos (request):
    try:
        if request.user.rol.rol == 'ventas' or request.user.rol.rol == 'gerencia':
            title = "Productos"
            productos=models.Productos.objects.all()
            return render (request, 'venta/productos.html',{'title':title, 'productos': productos})
        else:
            return redirect ('/')

    except:
        return redirect ('/')

@login_required
def producto_add (request):
    if request.method == 'POST':
         form = form_producto(request.POST)
         if form.is_valid():
            producto = models.Productos()
            producto.nombre = form.cleaned_data['nombre']
            producto.precio = form.cleaned_data['precio']
            producto.lente = form.cleaned_data['lente']
            producto.armazon = False
            if form.cleaned_data['lente']:
                producto.distancia = form.cleaned_data['distancia']
                producto.lado = form.cleaned_data['lado']
                producto.armazon = form.cleaned_data['armazon']
            producto.save()
            return redirect(reverse('productos'))
    try:
        if request.user.rol.rol == 'ventas':
            title = "Nuevo Producto"
            producto = models.Productos
            form = form_producto()
            return render (request, 'venta/producto_add_edit.html',{'title':title,'form':form})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def producto_edit (request, id_p):
    if request.method == 'POST':
         form = form_producto(request.POST)
         if form.is_valid():
            producto = models.Productos.objects.get(id=id_p)
            producto.nombre = form.cleaned_data['nombre']
            producto.precio = form.cleaned_data['precio']
            producto.lente = form.cleaned_data['lente']
            producto.armazon = False
            producto.distancia = '-'
            producto.lado ='-'
            if form.cleaned_data['lente']:
                producto.distancia = form.cleaned_data['distancia']
                producto.lado = form.cleaned_data['lado']
                producto.armazon = form.cleaned_data['armazon']
            producto.save()
            return redirect(reverse('productos'))
    try:
        if request.user.rol.rol == 'ventas':
            title = "Producto"
            producto = models.Productos.objects.get(id=id_p)
            form = form_producto({'nombre':producto.nombre,'precio':producto.precio,'lente':producto.lente,'distancia':producto.distancia,'lado':producto.lado,'armazon':producto.armazon})
            return render (request, 'venta/producto_add_edit.html',{'title':title,'form':form, 'edit':1, 'id_p':id_p})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def producto_del (request, id_p):
    try:
        if request.user.rol.rol == 'ventas':
            producto = models.Productos.objects.get(id=id_p).delete()
            return redirect(reverse('productos'))
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def pedidos (request):
    try:
        if request.user.rol.rol == 'ventas' or request.user.rol.rol == 'taller' or request.user.rol.rol == 'gerencia':
            title = "Pedidos"
            if request.user.rol.rol != 'taller':
                pedidos=models.Pedido.objects.all()
            else:
                #pedidos=models.Pedido.objects.filter(Q(estado='taller') | Q(estado='finalizado'))
                pedidos=models.Pedido.objects.filter(estado='taller') | models.Pedido.objects.filter(estado='finalizado')
            return render (request, 'venta/pedidos.html',{'title':title, 'pedidos': pedidos})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def pedido_add (request):
    if request.method == 'POST':
         form = form_pedido(request.POST)
         if form.is_valid():
            pedido = models.Pedido()
            pedido.vendedor = request.user
            pedido.paciente = Paciente.objects.get(id=form.cleaned_data['cliente'])
            pedido.pago = form.cleaned_data['pago']
            pedido.estado = 'pendiente'
            pedido.save()
            return redirect(reverse('pedido_edit', args=[pedido.id] ))
    # try:
    if request.user.rol.rol == 'ventas':
        title = "Nuevo Pedido"
        # productos = models.Productos.objects.all().order_by('nombre')
        form = form_pedido()
        return render (request, 'venta/pedido_add_edit.html',{'title':title,'form':form})
    else:
        return redirect ('/')
    # except:
    #     return redirect ('/')

@login_required
def pedido_edit (request, id_p):
    if request.method == 'POST':
        pedido = models.Pedido.objects.get(id=id_p)
        if request.user.rol.rol != 'taller':
            pedido.pago = request.POST['pago']
        pedido.estado = request.POST['estado']
        pedido.save()
#         return redirect(reverse('productos'))
    try:
        if request.user.rol.rol == 'ventas' or request.user.rol.rol == 'taller' or request.user.rol.rol == 'gerencia':
            title = "Pedido"
            pedido = models.Pedido.objects.get(id=id_p)
            form = form_pedido({'pago':pedido.pago})
            if request.user.rol.rol != 'taller':
                form_estado = form_pedido_estado({'estado':pedido.estado})
            else:
                form_estado = form_estado_taller({'estado':pedido.estado})
            lista = models.PedidoProducto.objects.filter(pedido=pedido)
            return render (request, 'venta/pedido_add_edit.html',{'title':title,'form':form, 'form_estado':form_estado, 'pedido':pedido, 'lista':lista, 'edit':1})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def pedido_del (request, id_p):
    try:
        if request.user.rol.rol == 'ventas':
            pedido = models.Pedido.objects.get(id=id_p)
            if pedido.estado != 'finalizado':
                pedido.delete()
            return redirect(reverse('pedidos'))
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def item_add (request, id_p):
    if request.method == 'POST':
         form = form_item_add(request.POST)
         if form.is_valid():
            pedido_producto = models.PedidoProducto()
            pedido_producto.pedido = models.Pedido.objects.get(id=id_p)
            pedido_producto.producto = models.Productos.objects.get(id=form.cleaned_data['producto'])
            pedido_producto.cantidad = form.cleaned_data['cantidad']
            pedido_producto.save()
            return redirect(reverse('pedido_edit', args=[id_p] ))
    try:
        if request.user.rol.rol == 'ventas':
            title = "Añadir Producto"
            form = form_item_add({'cantidad':1})
            return render (request, 'venta/item_add.html',{'title':title,'form':form})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

def item_del (request, id_p, id_i):
    try:
        if request.user.rol.rol == 'ventas':
            models.PedidoProducto.objects.get(id=id_i).delete()
            return redirect(reverse('pedido_edit', args=[id_p] ))
        else:
            return redirect ('/')
    except:
        return redirect ('/')