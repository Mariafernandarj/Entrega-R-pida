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


        # FLUJO EXCEPCIONAL 2: falla del servidor
        if nuevo_nombre == 'Falla': 
            messages.error(request, "Error: Falla del servidor. Intente más tarde.")
            return render(request, 'editar_comercio.html')
            
        # FLUJO EXCEPCIONAL 1: los datos ya existen
        if nuevo_nombre == restaurante_actual.nombre:
            messages.warning(request, "Datos ya existentes, por favor ingresa unos datos nuevos.")
            return render(request, 'editar_comercio.html')
        if nueva_contrasena == restaurante_actual.contrasena:
            messages.warning(request, "Datos ya existentes, por favor ingresa unos datos nuevos.")
            return render(request, 'editar_comercio.html')
            
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