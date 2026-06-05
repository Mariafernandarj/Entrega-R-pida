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
    # para guardar el producto en la sesion o BD temporal.
    return render(request, 'agregar_carrito.html')

def pago_producto(request):
    # Pantalla para seleccionar el metodo de pago
    return render(request, 'pago_producto.html')

def pago_tarjeta(request):
    if request.user.is_authenticated:
        # se busca el platillo mas reciente que el cliente haya seleccionado y que este en pendiente
        pedido_actual = Pedido.objects.filter(cliente__nombre_usuario=request.user.username, estado='pendiente').order_by('-id').first()
        
        if pedido_actual:
            # nombre del platillo al pedido para que sea el campo del cargo
            detalle = DetallePedido.objects.filter(pedido=pedido_actual).first()
            if detalle:
                pedido_actual.platillo = detalle.platillo
            
            # cuando el usuario le haya dadp al boton de aceptar
            if request.method == 'POST':
                # se cambia la columna a true cuando ya se haya pagado
                pedido_actual.pagado = True
                pedido_actual.save()
                
                messages.success(request, "¡Pago exitoso con Tarjeta! Tu pedido está en preparación.")
                return redirect('pagina_principal') # O a la pantalla de éxito que decidas
                
            # Si solo entro a ver la pantalla, se le manda los datos
            return render(request, 'pago_tarjeta.html', {'pedido': pedido_actual})
            
    # Si no hay pedido o no hay sesion, se regresa a pago con trjeta
    return redirect('pago_tarjeta.html')

def pago_transferencia(request):
    if request.user.is_authenticated:
        pedido_actual = Pedido.objects.filter(cliente__nombre_usuario=request.user.username, estado='pendiente').order_by('-id').first()
        
        if pedido_actual:
            detalle = DetallePedido.objects.filter(pedido=pedido_actual).first()
            if detalle:
                pedido_actual.platillo = detalle.platillo
                
            if request.method == 'POST':
                # se cambia la columna a true cuando ya se haya pagado
                pedido_actual.pagado = True
                pedido_actual.save()
                
                messages.success(request, "¡Transferencia exitosa! Tu pedido está en preparación.")
                return redirect('pagina_principal') 
                
            return render(request, 'pago_transferencia.html', {'pedido': pedido_actual})
            
    return redirect('pago_transferencia.html')