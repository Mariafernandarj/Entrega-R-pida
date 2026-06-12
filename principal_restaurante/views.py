from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from registrar_cuenta.models import Usuario
from navegar_menus.models import Restaurante, Platillo

def principal_restaurante(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')
    try:
        cuenta = Usuario.objects.get(nombre_usuario=request.user.username)
        if cuenta.tipo_usuario != 'restaurante':
            messages.error(request, 'Acceso denegado: esta área es solo para restaurantes.')
            return redirect('inicio_sesion')
        Restaurante.objects.get_or_create(
            nombre_usuario_dueno=request.user.username,
            defaults={
                'nombre': request.user.username
            }
        )
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')
    
    return render(request, 'principal_restaurante.html')


# ─────────────────────────────────────────────
#  CASO DE USO: GESTIONAR MENÚ
# ─────────────────────────────────────────────

def gestion_menu(request):
    # FLUJO EXCEPCIONAL E-1: usuario no autenticado
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    try:
        cuenta = Usuario.objects.get(nombre_usuario=request.user.username)
        if cuenta.tipo_usuario != 'restaurante':
            messages.error(request, 'Acceso denegado.')
            return redirect('pagina_principal')
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')

    # FLUJO EXCEPCIONAL E-2: restaurante no configurado
    try:
        restaurante = Restaurante.objects.get(nombre_usuario_dueno=request.user.username)
    except Restaurante.DoesNotExist:
        messages.error(request, 'No tienes un perfil de restaurante configurado.')
        return redirect('principal_restaurante')

    # Paso 2: cargar lista de platillos del restaurante
    platillos = Platillo.objects.filter(restaurante=restaurante)

    return render(request, 'gestion_menu.html', {
        'restaurante': restaurante,
        'platillos': platillos,
    })


def agregar_platillo(request):
    # FLUJO EXCEPCIONAL E-1: usuario no autenticado
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    try:
        restaurante = Restaurante.objects.get(nombre_usuario_dueno=request.user.username)
    except Restaurante.DoesNotExist:
        messages.error(request, 'No tienes un perfil de restaurante.')
        return redirect('principal_restaurante')

    if request.method == 'POST':
        nombre     = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio     = request.POST.get('precio', '').strip()
        imagen      = request.FILES.get('imagen')

        # FLUJO ALTERNATIVO A-1: campos obligatorios vacíos
        if not nombre or not precio:
            messages.warning(request, 'El nombre y el precio son obligatorios.')
            return redirect('gestion_menu')

        # FLUJO ALTERNATIVO A-2: precio no numérico o negativo
        try:
            precio_decimal = float(precio)
            if precio_decimal <= 0:
                raise ValueError
        except ValueError:
            messages.warning(request, 'El precio debe ser un número mayor a 0.')
            return redirect('gestion_menu')

        # FLUJO NORMAL: Paso 3-4 — guardar y mostrar mensaje de éxito
        try:
            Platillo.objects.create(
                restaurante=restaurante,
                nombre=nombre,
                descripcion=descripcion,
                precio=precio_decimal,
                agotado=False,
                imagen=imagen,
            )
            messages.success(request, f'Producto "{nombre}" agregado correctamente.')
        except Exception:
            # FLUJO EXCEPCIONAL E-2: falla del servidor
            messages.error(request, 'Error del servidor. No se pudo guardar el producto. Intenta de nuevo.')

    return redirect('gestion_menu')


def editar_platillo(request, platillo_id):
    # FLUJO EXCEPCIONAL E-1: usuario no autenticado
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    try:
        restaurante = Restaurante.objects.get(nombre_usuario_dueno=request.user.username)
    except Restaurante.DoesNotExist:
        return redirect('principal_restaurante')

    # FLUJO EXCEPCIONAL E-3: platillo no existe o no pertenece a este restaurante
    platillo = get_object_or_404(Platillo, id=platillo_id, restaurante=restaurante)

    if request.method == 'POST':
        nombre      = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio      = request.POST.get('precio', '').strip()

        # FLUJO ALTERNATIVO A-1: campos obligatorios vacíos
        if not nombre or not precio:
            messages.warning(request, 'El nombre y el precio son obligatorios.')
            return redirect('gestion_menu')

        # FLUJO ALTERNATIVO A-2: precio inválido
        try:
            precio_decimal = float(precio)
            if precio_decimal <= 0:
                raise ValueError
        except ValueError:
            messages.warning(request, 'El precio debe ser un número mayor a 0.')
            return redirect('gestion_menu')

        # FLUJO NORMAL: Paso 5-6 — actualizar y mostrar mensaje de éxito
        try:
            platillo.nombre      = nombre
            platillo.descripcion = descripcion
            platillo.precio      = precio_decimal
            nueva_imagen = request.FILES.get('imagen')
            if nueva_imagen:
                platillo.imagen = nueva_imagen
            platillo.save()
            messages.success(request, f'Cambios guardados con éxito para "{platillo.nombre}".')
        except Exception:
            # FLUJO EXCEPCIONAL E-2: falla del servidor
            messages.error(request, 'Error del servidor. No se pudieron guardar los cambios. Intenta de nuevo.')

    return redirect('gestion_menu')


def cambiar_disponibilidad(request, platillo_id):
    # FLUJO EXCEPCIONAL E-1: usuario no autenticado
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    try:
        restaurante = Restaurante.objects.get(nombre_usuario_dueno=request.user.username)
    except Restaurante.DoesNotExist:
        return redirect('principal_restaurante')

    platillo = get_object_or_404(Platillo, id=platillo_id, restaurante=restaurante)

    if request.method == 'POST':
        # FLUJO NORMAL N-4: toggle disponibilidad
        # Al desactivar, el platillo deja de aparecer para los clientes
        platillo.agotado = not platillo.agotado
        platillo.save()
        estado = 'No disponible' if platillo.agotado else 'Disponible'
        messages.success(request, f'"{platillo.nombre}" ahora está: {estado}.')

    return redirect('gestion_menu')