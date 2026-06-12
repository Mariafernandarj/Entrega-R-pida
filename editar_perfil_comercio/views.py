from django.shortcuts import render, redirect
from django.contrib import messages
from navegar_menus.models import Restaurante
from django.contrib.auth import update_session_auth_hash #para que Django no cierre sesion al cambiar la contraseña
from registrar_cuenta.models import Usuario
from solicitudes_reparto.models import Repartidor

def ver_perfil(request):
    # se cargan los datos reales de la BD
    #se busca al restaurante que se llame igual al nombre de ususario que haya iniciado sesion
    restaurante_actual = Restaurante.objects.filter(nombre=request.user.username).first()
    if not restaurante_actual:
        restaurante_actual = Restaurante.objects.create(nombre=request.user.username)
    contexto = {
        'restaurante': restaurante_actual
    }
    return render(request, 'perfil_comercio.html', contexto)

def editar_perfil(request):
    #muestra el restaurante a ser editado
    #muestra los datos especificos del uduario que tenga la sesion abierta
    restaurante_actual = Restaurante.objects.filter(nombre=request.user.username).first()
    if not restaurante_actual:
        restaurante_actual = Restaurante.objects.create(nombre=request.user.username)

    if request.method == 'POST':
        # loq ue el usuario escribe en e formulario
        nuevo_nombre = request.POST.get('nombre')
        nueva_direccion = request.POST.get('direccion')
        nuevo_telefono = request.POST.get('telefono')
        nueva_contrasena = request.POST.get('contrasena')
        
        #para que cuando haya errores no se borren los datos
        contexto = {'restaurante': restaurante_actual}

        # FLUJO EXCEPCIONAL: falla del servidor
        if nuevo_nombre == 'Falla': 
            messages.error(request, "Error: Falla del servidor. Intente más tarde.")
            return render(request, 'editar_comercio.html', contexto)
            
        # FLUJO ALTERNATIVO: los datos ya existen en otro restaurante
        #se filtran los restaurantes de la base de datos y se excluye al restaurante actual
        otros_restaurantes = Restaurante.objects.exclude(nombre=restaurante_actual.nombre)
        
        #se revisa si haya algun restaurante con la direccion nueva
        if nueva_direccion and otros_restaurantes.filter(direccion=nueva_direccion).exists():
            messages.warning(request, "La dirección ya está registrada en otro comercio. Por favor ingresa una diferente.")
            return render(request, 'editar_comercio.html', contexto)
        
        #se revisa si haya algun restaurante con el telefono nuevo
        if nuevo_telefono and otros_restaurantes.filter(telefono=nuevo_telefono).exists():
            messages.warning(request, "El teléfono ya está registrado en otro comercio. Por favor ingresa uno diferente.")
            return render(request, 'editar_comercio.html', contexto)
        
        #se revisa si haya algun restaurante con la nueva contraseña
        if nueva_contrasena and otros_restaurantes.filter(contrasena=nueva_contrasena).exists():
            messages.warning(request, "La contraseña ya está registrada en otro comercio. Por favor ingresa una diferente.")
            return render(request, 'editar_comercio.html', contexto)
            
        # FLUJO NORMAL: Se conecta, guarda datos en la base de datos temporal
        if restaurante_actual:
            restaurante_actual.nombre = nuevo_nombre
            restaurante_actual.direccion = nueva_direccion
            restaurante_actual.telefono = nuevo_telefono
            restaurante_actual.contrasena = nueva_contrasena
            nueva_imagen = request.FILES.get('imagen')
            if nueva_imagen:
                restaurante_actual.imagen = nueva_imagen
            restaurante_actual.save()

        #se actualiza la tabla general de usuarios, si se csmbis nombre o contraseña en editar perfilm entonces se actualiza para iniciar sesion
        user = request.user
        user.username = nuevo_nombre
        if nueva_contrasena: # Si se escribe una contraseña nueva, se sincroniza
            user.set_password(nueva_contrasena)
        user.save()
        
        # se mantiene la sesion abierta
        update_session_auth_hash(request, user)
            
        messages.success(request, "Tus datos han sido guardados exitosamente.")
        return redirect('perfil_comercio')
    
    contexto = {
            'restaurante': restaurante_actual
    }

    return render(request, 'editar_comercio.html', contexto)

def editar_cliente(request):
    # FLUJO EXCEPCIONAL E-1: no autenticado
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    try:
        usuario = Usuario.objects.get(nombre_usuario=request.user.username)
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')

    if request.method == 'POST':
        nuevo_nombre  = request.POST.get('nombre_usuario', '').strip()
        nuevo_tel     = request.POST.get('telefono', '').strip()
        nueva_dir     = request.POST.get('direccion', '').strip()
        nueva_tarjeta = request.POST.get('tarjeta', '').strip()
        nueva_contra  = request.POST.get('contrasena', '').strip()

        contexto = {'usuario': usuario}

        # FLUJO ALTERNATIVO A-2: campos obligatorios vacíos
        errores = {}
        if not nuevo_nombre:
            errores['nombre_usuario'] = True
        if not nuevo_tel:
            errores['telefono'] = True
        if errores:
            messages.warning(request, "Por favor completa todos los campos requeridos.")
            contexto['errores'] = errores
            return render(request, 'editar_datos_cliente.html', contexto)

        # FLUJO ALTERNATIVO A-3: formato de teléfono incorrecto
        if not nuevo_tel.isdigit() or len(nuevo_tel) != 10:
            messages.warning(request, "Formato de teléfono inválido (solo 10 números).")
            contexto['errores'] = {'telefono': True}
            return render(request, 'editar_datos_cliente.html', contexto)

        # FLUJO ALTERNATIVO A-1: nombre de usuario duplicado
        if nuevo_nombre != usuario.nombre_usuario:
            if Usuario.objects.filter(nombre_usuario=nuevo_nombre).exists():
                messages.warning(request, "Username no disponible, ya está tomado por otro usuario.")
                return render(request, 'editar_datos_cliente.html', contexto)

        try:
            # FLUJO NORMAL: guardar cambios
            usuario.nombre_usuario = nuevo_nombre
            usuario.telefono  = nuevo_tel
            usuario.direccion = nueva_dir
            usuario.tarjeta   = nueva_tarjeta
            if nueva_contra:
                usuario.contrasena = nueva_contra
            usuario.save()

            # Sincronizar con User de Django
            user = request.user
            user.username = nuevo_nombre
            if nueva_contra:
                user.set_password(nueva_contra)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, "¡Éxito! Tus datos han sido editados correctamente.")
            return redirect('pagina_principal')

        except Exception:
            # FLUJO EXCEPCIONAL E-1: falla del servidor
            messages.error(request, "Falla técnica: No se pudo conectar con el servidor. Sus cambios no han sido guardados, intente de nuevo más tarde.")
            return render(request, 'editar_datos_cliente.html', {'usuario': usuario})

    return render(request, 'editar_datos_cliente.html', {'usuario': usuario})


def editar_repartidor(request):
    # FLUJO EXCEPCIONAL E-1: no autenticado
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    try:
        usuario = Usuario.objects.get(nombre_usuario=request.user.username)
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')

    repartidor = Repartidor.objects.filter(nombre_usuario_repartidor=request.user.username).first()

    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre_usuario', '').strip()
        nuevo_tel    = request.POST.get('telefono', '').strip()
        nuevo_veh    = request.POST.get('vehiculo', '').strip()
        nuevas_placas = request.POST.get('placas', '').strip()
        nueva_clabe  = request.POST.get('clabe', '').strip()
        nueva_contra = request.POST.get('contrasena', '').strip()

        contexto = {'usuario': usuario, 'repartidor': repartidor}

        # FLUJO ALTERNATIVO A-2: campos obligatorios vacíos
        errores = {}
        if not nuevo_nombre:
            errores['nombre_usuario'] = True
        if not nuevo_tel:
            errores['telefono'] = True
        if errores:
            messages.warning(request, "Por favor completa todos los campos requeridos.")
            contexto['errores'] = errores
            return render(request, 'editar_datos_repartidor.html', contexto)

        # FLUJO ALTERNATIVO A-3: formato de teléfono incorrecto
        if not nuevo_tel.isdigit() or len(nuevo_tel) != 10:
            messages.warning(request, "Formato de teléfono inválido (solo 10 números).")
            contexto['errores'] = {'telefono': True}
            return render(request, 'editar_datos_repartidor.html', contexto)

        # FLUJO ALTERNATIVO A-3: formato de CLABE incorrecto
        if nueva_clabe and (not nueva_clabe.isdigit() or len(nueva_clabe) != 18):
            messages.warning(request, "La CLABE interbancaria debe tener exactamente 18 dígitos.")
            contexto['errores'] = {'clabe': True}
            return render(request, 'editar_datos_repartidor.html', contexto)

        # FLUJO ALTERNATIVO A-1: nombre de usuario duplicado
        if nuevo_nombre != usuario.nombre_usuario:
            if Usuario.objects.filter(nombre_usuario=nuevo_nombre).exists():
                messages.warning(request, "Username no disponible, ya está tomado por otro usuario.")
                return render(request, 'editar_datos_repartidor.html', contexto)

        try:
            # FLUJO NORMAL: guardar en Usuario
            usuario.nombre_usuario = nuevo_nombre
            if nueva_contra:
                usuario.contrasena = nueva_contra
            usuario.save()

            # Guardar en Repartidor
            if repartidor:
                repartidor.nombre                    = nuevo_nombre
                repartidor.nombre_usuario_repartidor = nuevo_nombre
                repartidor.telefono  = nuevo_tel
                repartidor.vehiculo  = nuevo_veh
                repartidor.placas    = nuevas_placas
                repartidor.clabe     = nueva_clabe
                repartidor.save()

            # Sincronizar con User de Django
            user = request.user
            user.username = nuevo_nombre
            if nueva_contra:
                user.set_password(nueva_contra)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, "¡Éxito! Tus datos han sido editados correctamente.")
            return redirect('principal_repartidor')

        except Exception:
            # FLUJO EXCEPCIONAL E-1: falla del servidor
            messages.error(request, "Falla técnica: No se pudo conectar con el servidor. Sus cambios no han sido guardados, intente de nuevo más tarde.")
            return render(request, 'editar_datos_repartidor.html', {'usuario': usuario, 'repartidor': repartidor})

    return render(request, 'editar_datos_repartidor.html', {'usuario': usuario, 'repartidor': repartidor})