from django.shortcuts import render
from django.contrib import messages
from registrar_cuenta.models import Usuario
from navegar_menus.models import Restaurante

def principal_restaurante(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')
    try:
        cuenta = Usuario.objects.get(nombre_usuario=request.user.username)
        if cuenta.tipo_usuario != 'restaurante':
            messages.error(request, 'Acceso denegado: esta área es solo para restaurantes.')
            return redirect('inicio')
        Restaurante.objects.get_or_create(
            nombre_usuario_dueno=request.user.username,
            defaults={
                'nombre': request.user.username
            }
        )
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')
    
    return render(request, 'principal_restaurante.html')
