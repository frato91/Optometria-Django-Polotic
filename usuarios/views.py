from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def Index(request):
    try:
        if request.user.rol.rol == 'secretaria':
            title = "secretaria".title().replace('i', 'í')
            return render (request, 'index.html',{'title':title})

        elif request.user.rol.rol == 'profecional_medico':
            title = "profecional_medico".title().replace('_', ' ')
            return render (request, 'index.html',{'title':title})

        elif request.user.rol.rol == 'ventas':
            title = "ventas".title()
            return render (request, 'index.html',{'title':title})

        elif request.user.rol.rol == 'taller':
            title = "taller".title()
            return render (request, 'index.html',{'title':title})

        elif request.user.rol.rol == 'gerencia':
            title = "gerencia".title()
            return render (request, 'index.html',{'title':title})

    except:
        title='Error'
        return render (request, 'error.html',{'title':title})

