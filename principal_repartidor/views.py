from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from registrar_cuenta.models import Usuario
from solicitudes_reparto.models import Repartidor

@never_cache
def principal_repartidor(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')
    try:
        cuenta = Usuario.objects.get(nombre_usuario=request.user.username)
        if cuenta.tipo_usuario != 'repartidor':
            messages.error( request, 'Acceso denegado: esta área es solo para repartidores.' )
            return redirect('inicio_sesion')
        #Crear perfil de repartidor si no existe
        Repartidor.objects.get_or_create(
            nombre_usuario_repartidor=request.user.username,
            defaults={
                'nombre': request.user.username
            }
        )
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')
    
    return render(request, 'principal_repartidor.html')