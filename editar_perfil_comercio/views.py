from django.shortcuts import render, redirect
from django.contrib import messages
from solicitudes_reparto.models import Restaurante

def ver_perfil(request):
    # se cargan los datos reales de la BD
    restaurante_actual = Restaurante.objects.first()
    contexto = {
        'restaurante': restaurante_actual
    }
    return render(request, 'perfil_comercio.html', contexto)

def editar_perfil(request):
    #de muestra el restaurante a ser editado
    restaurante_actual = Restaurante.objects.first()
    
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
        otros_restaurantes = Restaurante.objects.exclude(id=restaurante_actual.id)
        
        #se revisa si haya algun restaurante con la direccion nueva
        if otros_restaurantes.filter(direccion=nueva_direccion).exists():
            messages.warning(request, "La dirección ya está registrada en otro comercio. Por favor ingresa una diferente.")
            return render(request, 'editar_comercio.html', contexto)
        
        #se revisa si haya algun restaurante con el telefono nuevo
        if otros_restaurantes.filter(telefono=nuevo_telefono).exists():
            messages.warning(request, "El teléfono ya está registrado en otro comercio. Por favor ingresa uno diferente.")
            return render(request, 'editar_comercio.html', contexto)
        
        #se revisa si haya algun restaurante con la nueva contraseña
        if otros_restaurantes.filter(contrasena=nueva_contrasena).exists():
            messages.warning(request, "La contraseña ya está registrada en otro comercio. Por favor ingresa una diferente.")
            return render(request, 'editar_comercio.html', contexto)
            
        # FLUJO NORMAL: Se conecta, guarda datos en la base de datos temporal
        if restaurante_actual:
            restaurante_actual.nombre = nuevo_nombre
            restaurante_actual.direccion = nueva_direccion
            restaurante_actual.telefono = nuevo_telefono
            restaurante_actual.contrasena = nueva_contrasena
            restaurante_actual.save()
            
        messages.success(request, "Tus datos han sido guardados exitosamente.")
        return redirect('perfil_comercio')
    
    contexto = {
            'restaurante': restaurante_actual
    }

    return render(request, 'editar_comercio.html', contexto)