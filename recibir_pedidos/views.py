from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from solicitudes_reparto.models import Pedido
from navegar_menus.models import Restaurante 

@login_required(login_url='iniciar_sesion')
def revisar_pedidos_nuevos(request):
    # identificar si es reparrtidor o restaurante
    restaurante_actual = Restaurante.objects.filter(nombre=request.user.username).first()

    #Si no es un restaurante, no le busca nada
    if not restaurante_actual:
        return JsonResponse({'hay_nuevos': False, 'cantidad': 0})

    # Busca en la base de datos, cuantos pedidos hay pendientes para el restaurante
    # __iexact para que no le importen las mayúsculas o minúsculas
    cantidad_nuevos = Pedido.objects.filter(
        restaurante = restaurante_actual,
        estado__iexact='pendiente'
    ).count()

    # Le responde a la página
    return JsonResponse({
        'hay_nuevos': cantidad_nuevos > 0,
        'cantidad': cantidad_nuevos
    })