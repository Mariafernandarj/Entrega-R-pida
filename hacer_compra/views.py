from django.shortcuts import render, redirect
from django.contrib import messages

def platillo_seleccionado(request, id_platillo):
    # FLUJO NORMAL: consulta a la BD del platillo
    # platillo = Platillo.objects.get(id=id_platillo)
    
    contexto = {
        'id_platillo': id_platillo,
        'nombre_platillo': 'Hamburguesa Sencilla',
        'precio': 120.00
    }
    return render(request, 'platillo_seleccionado.html', contexto)

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