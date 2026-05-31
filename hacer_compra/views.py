from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
#para que funcione la base de datos
from navegar_menus.models import Platillo
from registrar_cuenta.models import Usuario
from solicitudes_reparto.models import Pedido, DetallePedido

def platillo_seleccionado(request, id_platillo):
    # FLUJO NORMAL: consulta a la BD del platillo
    # platillo = Platillo.objects.get(id=id_platillo)
    platillo_seleccionado = get_object_or_404(Platillo, id=id_platillo)
    
    contexto = {
        'platillo': platillo_seleccionado,
    }
    return render(request, 'platillo_seleccionado.html', contexto)

#para crear el pedido cuando se le da click en el boton
def adquirir_ahora(request, id_platillo):
    if request.method == 'POST':
        platillo = get_object_or_404(Platillo, id=id_platillo)
        
        if request.user.is_authenticated:
            # se identifica al cliente
            cliente = Usuario.objects.get(nombre_usuario=request.user.username)
            
            #se crea el pedido (tiket) en la base de datos
            nuevo_pedido = Pedido.objects.create(
                cliente=cliente,
                restaurante_id=platillo.restaurante.id,
                estado='pendiente',
                total=platillo.precio
            )
            
            # se agregael platillo a ese ticket
            DetallePedido.objects.create(
                pedido=nuevo_pedido,
                platillo=platillo,
                cantidad=1,
                subtotal=platillo.precio
            )
            
            messages.success(request, f"¡Tu pedido de {platillo.nombre} ha sido creado con éxito!")
            # cuando ya lo agrego a la base de datos entonces manda a las opciones de pago
            return redirect('pago_producto')
        
        # Si se intenta entrar sin darle clic al boton, se regresa
    return redirect('pagina_principal')

def agregar_carrito(request):
    # logica del Controlador 'AgregarCarritoControlador'
    # para guardar el producto en la sesión o BD temporal.
    return render(request, 'agregar_carrito.html')

def pago_producto(request):
    # Pantalla para seleccionar el método de pago
    return render(request, 'pago_producto.html')

def pago_tarjeta(request):
    if request.method == 'POST':
        # FLUJO EXCEPCIONAL: Simulación de recursos insuficientes o caída del servidor
        # if not validacion_banco():
        #     messages.error(request, "Recursos insuficientes o error de conexión.")
        #     return render(request, 'pago_tarjeta.html')
        
        # FLUJO NORMAL: Compra exitosa
        messages.success(request, "¡Compra exitosa! Tu pedido está en camino.")
        return redirect('buscar_comida') 
        
    return render(request, 'pago_tarjeta.html')

def pago_transferencia(request):
    if request.method == 'POST':
        messages.success(request, "¡Transferencia validada y compra exitosa!")
        return redirect('buscar_comida')
        
    return render(request, 'pago_transferencia.html')