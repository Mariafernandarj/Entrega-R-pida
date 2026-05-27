from django.shortcuts import render
from navegar_menus.models import Restaurante, Platillo

def buscar_platillo(request):
    # capta y revisa lo que el usuario esceribió en el buscador
    texto_busqueda = request.GET.get('q', '').strip()
    
    resultados_platillos = []

    if texto_busqueda:
        # Busca en la base de datos 
        platillos_encontrados = Platillo.objects.filter(nombre__icontains=texto_busqueda)
            
        for platillo in platillos_encontrados:
            if getattr(platillo, 'restaurante', None):
                resultados_platillos.append({
                    'restaurante': platillo.restaurante,
                    'platillo': platillo
            })

    contexto = {
        'texto_busqueda': texto_busqueda,
        'resultados': resultados_platillos,
    }
    return render(request, 'busquedaPlatillo.html', context=contexto)

def restaurante_seleccionado(request, id):
    return render(request, 'restauranteSeleccionado.html', {'restaurante_id': id})