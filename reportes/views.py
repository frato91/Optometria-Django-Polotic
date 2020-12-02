from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.db.models import Q



from clinica.models import Paciente, User, Turno
from venta.models import Pedido, PedidoProducto, Productos

# Create your views here.
@login_required
def reportes (request):
    # try:
    if request.user.rol.rol == 'gerencia':
        title = "Reportes"
        return render (request, 'reportes/reportes.html',{'title':title})
    else:
        return redirect ('/')

    # except:
    #     return redirect ('/')
@login_required
def reportes_opciones (request, reporte):
    # try:
    if request.user.rol.rol == 'gerencia':
        title = "Reportes"
        if reporte == 1:
            turnos = Turno.objects.filter(Q(date__month=timezone.now().month) & Q(asistencia='asistio'))
            return render (request, 'reportes/reportes.html',{'title':title, 'reporte':reporte, 'turnos': turnos})
        elif reporte == 2:
            turnos = Turno.objects.filter(Q(date__month=timezone.now().month) & Q(asistencia='no_asistio'))
            return render (request, 'reportes/reportes.html',{'title':title, 'reporte':reporte, 'turnos': turnos})
        elif reporte == 3:
            pedidos = Pedido.objects.filter(creation__month=timezone.now().month)
            return render (request, 'reportes/reportes.html',{'title':title, 'reporte':reporte, 'pedidos': pedidos})
        elif reporte == 4:
            productos = Productos.objects.all()
            lista_cantidad = {}
            for producto in productos:
                lista_cantidad[producto.id]=0
                pedidos = Pedido.objects.filter(creation__month=timezone.now().month)
                for pedido in pedidos:
                    pedidoproductos=PedidoProducto.objects.filter(pedido=pedido)
                    for pedidoproducto in pedidoproductos:
                        if pedidoproducto.producto == producto:
                            lista_cantidad[producto.id]+=pedidoproducto.cantidad
            lista_ordenada=sortedDict = sorted(lista_cantidad.items(), key=lambda x: x[1], reverse=True)
            return render (request, 'reportes/reportes.html',{'title':title, 'reporte':reporte, 'productos': productos, 'lista_cantidad':lista_ordenada})
        elif reporte == 5:
            pedidos = Pedido.objects.all().order_by('creation')
            #Año
            years=[]
            for pedido in pedidos:
                existe=False
                for year in years:
                    if year == pedido.creation.year:
                        existe=True
                if not existe:
                    years.append (pedido.creation.year)
                if years == []:
                    years.append (pedido.creation.year)
            #MES
            months=[]
            for pedido in pedidos:
                existe=False
                for month in months:
                    if month == pedido.creation.month:
                        existe=True
                if not existe:
                    months.append (pedido.creation.month)
                if months == []:
                    months.append (pedido.creation.month)
            year_select=0
            month_select=0
            if request.method == 'POST':
                year_select=request.POST['year']
                month_select=request.POST['month']
                pedidos = Pedido.objects.filter(Q(creation__year=request.POST['year']) & Q(creation__month=request.POST['month'])).order_by('creation')
            datos=[]
            for pedido in pedidos:
                existe=False
                for dato in datos:
                    if dato[0]== pedido.vendedor.id:
                        existe=True
                        dato[2]+=1
                        dato[3]+=pedido.cantidad()
                if not existe:
                    datos.append([pedido.vendedor.id ,f"{pedido.vendedor.last_name.title()}, {pedido.vendedor.first_name.title()}",1,pedido.cantidad()])
                if datos == []:
                    datos.append([pedido.vendedor.id ,f"{pedido.vendedor.last_name.title()}, {pedido.vendedor.first_name.title()}",1,pedido.cantidad()])
            print (datos)
            return render (request, 'reportes/reportes.html',{'title':title, 'reporte':reporte, 'datos': datos, 'years':years, 'months':months,'year_select':int(year_select),'month_select':int(month_select)})
        else :
            return redirect ('/')
    else:
        return redirect ('/')

    # except:
    #     return redirect ('/')