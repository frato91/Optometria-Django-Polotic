from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from .models import Paciente, User, Turno, HistorialMedico
from .forms import form_pacientes, form_turnos, form_asistencia, form_historial_medico

# Create your views here.

@login_required
def pacientes (request):
    try:
        if request.user.rol.rol == 'secretaria' or request.user.rol.rol == 'gerencia':
            title = "Pacientes"
            pacientes=Paciente.objects.all()
            return render (request, 'clinica/pacientes.html',{'title':title, 'pacientes': pacientes})
        elif request.user.rol.rol == 'profecional_medico':
            title = "Pacientes"
            pacientes=Paciente.objects.filter(medico=request.user)
            return render (request, 'clinica/pacientes.html',{'title':title, 'pacientes': pacientes})
        else:
            return redirect ('/')

    except:
        return redirect ('/')

@login_required
def paciente_detail(request, id_p):

    try:
        paciente=Paciente.objects.get(id=id_p)
        title = f"{paciente.apellido}, {paciente.nombre}"
        turnos = Turno.objects.filter(paciente=paciente)
        historial_medico = HistorialMedico.objects.filter(paciente=paciente)
        if request.user.rol.rol == 'secretaria' or request.user.rol.rol == 'gerencia':
            return render (request, 'clinica/paciente_detail.html',{'title':title, 'paciente': paciente, 'turnos':turnos})
        elif request.user.rol.rol == 'profecional_medico':
            if paciente.medico != request.user:
                return redirect ('/')
            return render (request, 'clinica/paciente_detail.html',{'title':title, 'paciente': paciente, 'turnos':turnos, 'historial_medico':historial_medico})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def paciente_add (request):
    if request.method == 'POST':
        form = form_pacientes(request.POST)
        if form.is_valid():
            paciente = Paciente()
            paciente.nombre = form.cleaned_data['nombre']
            paciente.apellido = form.cleaned_data['apellido']
            paciente.dni = form.cleaned_data['dni']
            paciente.telefono = form.cleaned_data['telefono']
            user = User.objects.get(id=form.cleaned_data['medico'])
            paciente.medico = user
            paciente.save()
            return redirect(reverse('pacientes'))
    try:
        if request.user.rol.rol == 'secretaria':
            title = "Agregar un nuevo Paciente"
            form = form_pacientes()
            return render (request, 'clinica/paciente_add.html',{'title':title,'form':form})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def paciente_edit (request, id_p):
    if request.method == 'POST':
        form = form_pacientes(request.POST)
        if form.is_valid():
            paciente = Paciente.objects.get(id=id_p)
            paciente.nombre = form.cleaned_data['nombre']
            paciente.apellido = form.cleaned_data['apellido']
            paciente.dni = form.cleaned_data['dni']
            paciente.telefono = form.cleaned_data['telefono']
            user = User.objects.get(id=form.cleaned_data['medico'])
            paciente.medico = user
            paciente.save()
            return redirect(reverse('paciente_detail', args=[id_p]))
    try:
        if request.user.rol.rol == 'secretaria':
            title = "Editar Paciente"
            paciente = Paciente.objects.get(id=id_p)
            form = form_pacientes({'nombre':paciente.nombre, 'apellido':paciente.apellido, 'dni':paciente.dni, 'telefono':paciente.telefono,'medico':paciente.medico.id})
            return render (request, 'clinica/paciente_edit.html',{'title':title,'form':form, 'id_p':id_p})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def paciente_del (request, id_p):
    try:
        if request.user.rol.rol == 'secretaria':
            title = "Editar Paciente"
            paciente = Paciente.objects.get(id=id_p).delete()
            return redirect (reverse('pacientes'))
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def turnos_add (request, id_p):
    if request.method == 'POST':
        form = form_turnos(request.POST)
        if form.is_valid():
            paciente = Paciente.objects.get(id=id_p)
            turno = Turno()
            turno.paciente = paciente
            turno.medico = paciente.medico
            turno.date = f"{form.cleaned_data['date']} {form.cleaned_data['hour']}"
            hora = form.cleaned_data['hour']
            turno.save()
            return redirect(reverse('paciente_detail', args=(id_p,)))
    try:
        if request.user.rol.rol == 'secretaria':
            title = "Turnos"
            paciente = Paciente.objects.get(id=id_p)
            turno = Turno()
            turno.paciente = paciente
            turno.medico = paciente.medico
            form = form_turnos()
            return render (request, 'clinica/turno_add.html',{'title':title,'form':form, 'turno': turno})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def turnos_edit (request, id_p, id_turno):
    if request.method == 'POST':
        if request.user.rol.rol == 'secretaria':
            form = form_turnos(request.POST)
            if form.is_valid():
                turno = Turno.objects.get(id=id_turno)
                turno.date = f"{form.cleaned_data['date']} {form.cleaned_data['hour']}"
                hora = form.cleaned_data['hour']
                turno.save()
                return redirect(reverse('paciente_detail', args=(id_p,)))
        elif request.user.rol.rol == 'profecional_medico':
            form = form_asistencia(request.POST)
            if form.is_valid():
                turno = Turno.objects.get(id=id_turno)
                turno.asistencia = form.cleaned_data['asistencia']
                turno.save()
                return redirect(reverse('paciente_detail', args=(id_p,)))

        else:
            return redirect ('/')
    try:
        if request.user.rol.rol == 'secretaria':
            title = "Turnos"
            turno = Turno.objects.get(id=id_turno)
            form = form_turnos({'date':f"{str(turno.date.day).zfill(2)}/{str(turno.date.month).zfill(2)}/{str(turno.date.year).zfill(4)}",'hour':f"{str(turno.date.hour).zfill(2)}:{str(turno.date.minute).zfill(2)}"})
            return render (request, 'clinica/turno_add.html',{'title':title,'form':form, 'edit':1, 'turno':turno})
        elif request.user.rol.rol == 'profecional_medico':
            title = "Turnos"
            paciente = Paciente.objects.get(id=id_p)
            turno = Turno.objects.get(id=id_turno)
            form = form_asistencia({'asistencia':turno.asistencia})
            return render (request, 'clinica/turno_add.html',{'title':title,'form':form, 'edit':1, 'turno':turno})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def turnos_del (request, id_p, id_turno):
    try:
        if request.user.rol.rol == 'secretaria':
            turno = Turno.objects.get(id=id_turno).delete()
            return redirect (reverse('paciente_detail', args=(id_p,)))
        else:
            return redirect ('/')
    except:
        return redirect ('/')


@login_required
def turnos (request):
    try:
        if request.user.rol.rol == 'secretaria' or request.user.rol.rol == 'gerencia':
            title = "Turnos"
            turnos =Turno.objects.all()
            return render (request, 'clinica/turno.html',{'title':title, 'turnos': turnos})
        elif request.user.rol.rol == 'profecional_medico':
            title = "Turnos"
            turnos =Turno.objects.filter(medico=request.user)
            return render (request, 'clinica/turno.html',{'title':title, 'turnos': turnos})
        else:
            return redirect ('/')

    except:
        return redirect ('/')

@login_required
def historial_medico_add (request, id_p):
    if request.method == 'POST':
        form = form_historial_medico(request.POST)
        if form.is_valid():
            historial_medico = HistorialMedico()
            historial_medico.paciente = Paciente.objects.get(id=id_p)
            historial_medico.medico = request.user
            historial_medico.asunto = form.cleaned_data['asunto']
            historial_medico.descripcion = form.cleaned_data['descripcion']
            historial_medico.save()
            return redirect(reverse('paciente_detail', args=(id_p,)))
    try:
        if request.user.rol.rol == 'profecional_medico':
            title = "Historial Médico"
            historial_medico = HistorialMedico()
            historial_medico.paciente = Paciente.objects.get(id=id_p)
            historial_medico.medico = request.user
            form = form_historial_medico()
            return render (request, 'clinica/historial_medico.html',{'title':title,'form':form, 'historial_medico': historial_medico})
        else:
            return redirect ('/')
    except:
        return redirect ('/')

@login_required
def historial_medico_detail (request, id_p, id_hm):
    # try:
    if request.user.rol.rol == 'profecional_medico':
        title = "Historial Médico"
        historial_medico = HistorialMedico.objects.get(id=id_hm)
        return render (request, 'clinica/historial_medico.html',{'title':title, 'historial_medico': historial_medico, 'ver':1})
    else:
        return redirect ('/')
    # except:
    #     return redirect ('/')