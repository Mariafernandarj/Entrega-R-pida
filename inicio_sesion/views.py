from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from registrar_cuenta.models import Usuario #models de registrar_cuenta para usarlo

def iniciar_sesion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_usuario', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()
        
        print(f"DEBUG: Intentando entrar con {nombre}") #debug prueba
        
        # para validar los datos, e inicio de sesion
        user = authenticate(request, username=nombre, password=contrasena)
        
        #si falla, revisar que el usuario existe en la base de datos de registrar cuenta
        if user is None:
            usuario_tecnico = Usuario.objects.filter(nombre_usuario=nombre, contrasena=contrasena).first()
            
            if usuario_tecnico:
                
                print(f"DEBUG: Usuario {nombre} encontrado en la tabla personalizada. Sincronizando...") #deebug tambien
                
                user_oficial = User.objects.filter(username=nombre).first()
                
                if not user_oficial:
                    # Si no existe, lo creamos
                    User.objects.create_user(username=nombre, password=contrasena)
                else:
                    # Si ya existía pero no pudimos entrar (ej. cambió la contraseña), la actualizamos
                    user_oficial.set_password(contrasena)
                    user_oficial.save()

                # volver a autenticar para iniciar sesion
                user = authenticate(request, username=nombre, password=contrasena)
        
        if user is not None:
            login(request, user)
            # redirigir dependiendo del tipo de usuario, a pagina principal de cada caso
            info_usuario = Usuario.objects.filter(nombre_usuario=nombre).first()
            if info_usuario and info_usuario.tipo_usuario == 'restaurante':
                return redirect('perfil_comercio')
            else:
                return redirect('buscar_comida') 
        else:
            # Flujo alternativo, mensaje de error
            messages.error(request, "Nombre de usuario o contraseña incorrectos. Por favor, vuelve a intentarlo.")
            return redirect('iniciar_sesion')
            
    return render(request, 'inicioSesion.html')