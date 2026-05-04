from django.shortcuts import render
from django.contrib import messages
# from core.models import Restaurante, Platillo  (para los modelos)

def buscar_comida(request):
    texto_busqueda = request.GET.get('q', '')
    
    resultados_restaurantes = []
    resultados_platillos = []

    if texto_busqueda:
        try:
            # FLUJO NORMAL: Conecta a la BD y busca coincidencias
            # resultados_restaurantes = Restaurante.objects.filter(nombre__icontains=texto_busqueda)
            # resultados_platillos = Platillo.objects.filter(nombre__icontains=texto_busqueda)
            
            # FLUJO ALTERNATIVO: Si no hay resultados, manda un mensaje[cite: 2]
            # if not resultados_restaurantes and not resultados_platillos:
            #     messages.warning(request, f"No se encontraron resultados para '{texto_busqueda}'.")
            pass # Quita este 'pass' cuando descomentes lo de arriba
            
        except Exception as e:
            # FLUJO EXCEPCIONAL: Falla de conexión con la BD
            messages.error(request, "Mensaje con aviso de falla en el sistema. Intente más tarde.")

    # Manda los resultados a la pantalla busqueda_platillo
    contexto = {
        'texto_busqueda': texto_busqueda,
        'restaurantes': resultados_restaurantes,
        'platillos': resultados_platillos,
    }
    return render(request, 'busquedaPlatillo.html', contexto)

def restaurante_seleccionado(request, id):
    return render(request, 'restauranteSeleccionado.html', {'restaurante_id': id})