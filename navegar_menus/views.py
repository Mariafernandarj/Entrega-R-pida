from django.shortcuts import render, get_object_or_404
from .models import Restaurante, Platillo

def pagina_principal(request):
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