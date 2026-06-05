from django.shortcuts import render, get_object_or_404
from navegar_menus.models import Restaurante, Platillo

def buscar_platillo(request):
    # capta y revisa lo que el usuario esceribió en el buscador
    texto_busqueda = request.GET.get('q', '').strip()
    
    resultados_platillos = []
    resultados_restaurantes = []

    if texto_busqueda:
        # Busca en la base de datos 
        platillos_encontrados = Platillo.objects.filter(nombre__icontains=texto_busqueda)
            
        for platillo in platillos_encontrados:
            if getattr(platillo, 'restaurante', None):
                resultados_platillos.append({
                    'restaurante': platillo.restaurante,
                    'platillo': platillo
            })
    
        resultados_restaurantes = Restaurante.objects.filter(nombre__icontains=texto_busqueda)

    contexto = {
        'texto_busqueda': texto_busqueda,
        'resultados': resultados_platillos,
        'resultados_restaurantes': resultados_restaurantes
    }
    return render(request, 'busquedaPlatillo.html', context=contexto)

def restauranteSeleccionado(request, id_restaurante):
    # buscar el restaurante especifico
    restaurante = get_object_or_404(Restaurante, id=id_restaurante)
    
    # se buscan todos los platillos que le pertenecen a ese restaurante
    platillos = Platillo.objects.filter(restaurante=restaurante)
    
    # mandarlos a la pantalla
    return render(request, 'restauranteSeleccionado.html', {
        'restaurante': restaurante,
        'platillos': platillos
    })