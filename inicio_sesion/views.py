from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def iniciar_sesion(request):
    if request.method == 'POST':
        usuario_input = request.POST.get('usuario')
        contrasena_input = request.POST.get('contrasena')
        
        # Valida los datos
        user = authenticate(request, username=usuario_input, password=contrasena_input)
        
        if user is not None:
            login(request, user)
            # Redirige a la página principal tras un login exitoso
            return redirect('pagina_principal') # Asegúrate de que esta URL exista en core/urls.py
        else:
            # Flujo alternativo: Muestra mensaje de error
            messages.error(request, "Nombre de usuario o contraseña incorrectos. Por favor, vuelve a intentarlo.")
            return redirect('iniciar_sesion')
            
    return render(request, 'inicioSesion.html')