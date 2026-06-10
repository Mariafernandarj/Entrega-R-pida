from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from navegar_menus.models import Platillo
from registrar_cuenta.models import Usuario
from solicitudes_reparto.models import Pedido, DetallePedido


# ─────────────────────────────────────────────
#  HELPERS DE SESIÓN
# ─────────────────────────────────────────────

def _get_carrito(request):
    return request.session.get('carrito', {})

def _save_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True

def _calcular_total(carrito):
    return sum(float(item['precio']) * item['cantidad'] for item in carrito.values())


# ─────────────────────────────────────────────
#  VISTAS EXISTENTES (sin cambios)
# ─────────────────────────────────────────────

def platillo_seleccionado(request, id_platillo):
    platillo_sel = get_object_or_404(Platillo, id=id_platillo)
    return render(request, 'platillo_seleccionado.html', {'platillo': platillo_sel})


def adquirir_ahora(request, id_platillo):
    if request.method == 'POST':
        platillo = get_object_or_404(Platillo, id=id_platillo)
        if request.user.is_authenticated:
            cliente = Usuario.objects.get(nombre_usuario=request.user.username)
            nuevo_pedido = Pedido.objects.create(
                cliente=cliente,
                restaurante_id=platillo.restaurante.id,
                estado='pendiente',
                total=platillo.precio
            )
            DetallePedido.objects.create(
                pedido=nuevo_pedido,
                platillo=platillo,
                cantidad=1,
                subtotal=platillo.precio
            )
            messages.success(request, f"¡Tu pedido de {platillo.nombre} ha sido creado con éxito!")
            return redirect('pago_producto')
    return redirect('pagina_principal')


def pago_producto(request):
    return render(request, 'pago_producto.html')


def pago_tarjeta(request):
    if request.user.is_authenticated:
        pedido_actual = Pedido.objects.filter(
            cliente__nombre_usuario=request.user.username, estado='pendiente'
        ).order_by('-id').first()
        if pedido_actual:
            detalle = DetallePedido.objects.filter(pedido=pedido_actual).first()
            if detalle:
                pedido_actual.platillo = detalle.platillo
            if request.method == 'POST':
                pedido_actual.pagado = True
                pedido_actual.save()
                messages.success(request, "¡Pago exitoso con Tarjeta! Tu pedido está en preparación.")
                return redirect('pagina_principal')
            return render(request, 'pago_tarjeta.html', {'pedido': pedido_actual})
    return redirect('pago_tarjeta.html')


def pago_transferencia(request):
    if request.user.is_authenticated:
        pedido_actual = Pedido.objects.filter(
            cliente__nombre_usuario=request.user.username, estado='pendiente'
        ).order_by('-id').first()
        if pedido_actual:
            detalle = DetallePedido.objects.filter(pedido=pedido_actual).first()
            if detalle:
                pedido_actual.platillo = detalle.platillo
            if request.method == 'POST':
                pedido_actual.pagado = True
                pedido_actual.save()
                messages.success(request, "¡Transferencia exitosa! Tu pedido está en preparación.")
                return redirect('pagina_principal')
            return render(request, 'pago_transferencia.html', {'pedido': pedido_actual})
    return redirect('pago_transferencia.html')


# ─────────────────────────────────────────────
#  CASO DE USO: MODIFICAR CARRITO
# ─────────────────────────────────────────────

def agregar_carrito(request):
    # FLUJO EXCEPCIONAL E-1: usuario no autenticado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para ver tu carrito.")
        return redirect('iniciar_sesion')

    carrito = _get_carrito(request)
    total = _calcular_total(carrito)
    return render(request, 'agregar_carrito.html', {'carrito': carrito, 'total': total})


def agregar_producto_carrito(request, id_platillo):
    # FLUJO EXCEPCIONAL E-1: usuario no autenticado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para agregar productos al carrito.")
        return redirect('iniciar_sesion')

    platillo = get_object_or_404(Platillo, id=id_platillo)

    # FLUJO ALTERNATIVO A-1: platillo agotado
    if platillo.agotado:
        messages.warning(request, f"'{platillo.nombre}' no está disponible en este momento.")
        return redirect('restaurante_seleccionado', id_restaurante=platillo.restaurante.id)

    carrito = _get_carrito(request)
    key = str(id_platillo)

    # FLUJO ALTERNATIVO A-2: límite de 100 productos distintos
    if key not in carrito and len(carrito) >= 100:
        messages.warning(request, "Has alcanzado el límite de 100 productos diferentes en tu carrito.")
        return redirect('agregar_carrito')

    cantidad_actual = carrito[key]['cantidad'] if key in carrito else 0

    # FLUJO ALTERNATIVO A-3: límite de 100 unidades del mismo producto
    if cantidad_actual >= 100:
        messages.warning(request, "Solo puedes agregar hasta 100 unidades del mismo producto.")
        return redirect('agregar_carrito')

    # FLUJO NORMAL: agregar o incrementar
    if key in carrito:
        carrito[key]['cantidad'] += 1
    else:
        carrito[key] = {
            'nombre': platillo.nombre,
            'precio': str(platillo.precio),
            'cantidad': 1,
        }

    try:
        _save_carrito(request, carrito)
        messages.success(request, f"'{platillo.nombre}' agregado al carrito.")
    except Exception:
        # FLUJO EXCEPCIONAL E-2: error al guardar en sesión
        messages.error(request, "Error al guardar el carrito. Intenta de nuevo.")

    return redirect('agregar_carrito')


def modificar_carrito(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para modificar tu carrito.")
        return redirect('iniciar_sesion')

    if request.method != 'POST':
        return redirect('agregar_carrito')

    carrito = _get_carrito(request)
    accion = request.POST.get('accion')

    if accion == 'eliminar':
        id_platillo = request.POST.get('id_platillo')
        key = str(id_platillo)
        if key in carrito:
            nombre = carrito[key]['nombre']
            del carrito[key]
            try:
                _save_carrito(request, carrito)
                messages.success(request, f"'{nombre}' eliminado del carrito.")
            except Exception:
                messages.error(request, "Error al eliminar el producto. Intenta de nuevo.")
        else:
            messages.warning(request, "El producto que intentas eliminar ya no está en tu carrito.")
        return redirect('agregar_carrito')

    if accion == 'guardar':
        print("POST recibido:", dict(request.POST))
        carrito_actualizado = {}

        for key, item in carrito.items():
            valor = request.POST.get(f"cantidad_{key}", '').strip()

            if not valor or not valor.isdigit():
                messages.warning(request, f"Cantidad inválida para '{item['nombre']}'.")
                continue

            nueva_cantidad = int(valor)

            if nueva_cantidad > 100:
                messages.warning(request, f"'{item['nombre']}' no puede superar las 100 unidades.")
                continue

            if nueva_cantidad == 0:
                continue

            carrito_actualizado[key] = {
                'nombre': item['nombre'],
                'precio': item['precio'],
                'cantidad': nueva_cantidad,
            }

        try:
            _save_carrito(request, carrito_actualizado)
            total_nuevo = _calcular_total(carrito_actualizado)
            messages.success(request, f"Carrito actualizado. Total: ${total_nuevo:.2f}")
        except Exception:
            messages.error(request, "Error del servidor al guardar los cambios. Intenta de nuevo.")

        return redirect('agregar_carrito')

    messages.warning(request, "Acción no reconocida.")
    return redirect('agregar_carrito')