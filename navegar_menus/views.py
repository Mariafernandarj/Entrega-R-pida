from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from .models import Restaurante, Platillo

def pagina_principal(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')
    restaurantes = Restaurante.objects.all()
    platillos = Platillo.objects.all()
    return render(request, 'navegar_menus/pagina_principal.html', {
        'restaurantes': restaurantes,
        'platillos': platillos,
    })

def detalle_platillo(request, platillo_id):
    platillo = get_object_or_404(Platillo, id=platillo_id)
    return render(request, 'navegar_menus/detalle_platillo.html', {
        'platillo': platillo,
    })

def cerrar_sesion(request):
    logout(request)
    response = redirect('iniciar_sesion')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response