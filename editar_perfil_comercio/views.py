from django.shortcuts import render, redirect
from django.contrib import messages

def ver_perfil(request):
    # se cargan los datos reales de la BD
    contexto = {
        'nombre_restaurante': request.session.get('nombre_restaurante', 'Mi Gran Restaurante'),
        'direccion': request.session.get('direccion', 'Av. Principal 123'),
        'telefono': request.session.get('telefono', '555-1234')
    }
    return render(request, 'perfil_comercio.html', contexto)

def editar_perfil(request):
    if request.method == 'POST':
        # loq ue el usuario escribe en e formulario
        nuevo_nombre = request.POST.get('nombre')
        nueva_direccion = request.POST.get('direccion')
        nuevo_telefono = request.POST.get('telefono')

        # FLUJO EXCEPCIONAL 2: falla del servidor
        if nuevo_nombre == 'Falla': 
            messages.error(request, "Error: Falla del servidor. Intente más tarde.")
            return render(request, 'editar_comercio.html')
            
        # FLUJO EXCEPCIONAL 1: los datos ya existen
        if nuevo_nombre == 'Mi Gran Restaurante':
            messages.warning(request, "Datos ya existentes, por favor ingresa unos datos nuevos.")
            return render(request, 'editar_comercio.html')
            
        # FLUJO NORMAL: Se conecta, guarda datos en la base de datos temporal
        request.session['nombre_restaurante'] = nuevo_nombre
        request.session['direccion'] = nueva_direccion
        request.session['telefono'] = nuevo_telefono
        
        messages.success(request, "Tus datos han sido guardados exitosamente.")
        return redirect('perfil_comercio')

    return render(request, 'editar_comercio.html')