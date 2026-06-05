from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from registrar_cuenta.models import Usuario #models de registrar_cuenta para usarlo
from django.contrib.auth.views import LogoutView #para cerrar sesion
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def iniciar_sesion(request):       
    if request.user.is_authenticated:
            return redirect('pagina_principal')  
    if request.method == 'POST':        
        if request.user.is_authenticated:
            return redirect('pagina_principal') 

        nombre = request.POST.get('nombre_usuario', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()
        
        print(f"DEBUG: Intentando entrar con {nombre}") 
        
        user = authenticate(request, username=nombre, password=contrasena)
        
        if user is None:
            usuario_tecnico = Usuario.objects.filter(nombre_usuario=nombre, contrasena=contrasena).first()
            
            if usuario_tecnico:
                print(f"DEBUG: Usuario {nombre} encontrado en la tabla personalizada. Sincronizando...") 
                
                user_oficial = User.objects.filter(username=nombre).first()
                
                if not user_oficial:
                    User.objects.create_user(username=nombre, password=contrasena)
                else:
                    user_oficial.set_password(contrasena)
                    user_oficial.save()

                user = authenticate(request, username=nombre, password=contrasena)
        
        if user is not None:
            login(request, user)
            info_usuario = Usuario.objects.filter(nombre_usuario=nombre).first()
            if info_usuario:
                print(f"DEBUG: Usuario identificado como tipo: {info_usuario.tipo_usuario}")
                
                if info_usuario.tipo_usuario == 'repartidor':
                    return redirect('principal_repartidor')
                
                elif info_usuario.tipo_usuario == 'restaurante':
                    return redirect('principal_restaurante')  
                
                elif info_usuario.tipo_usuario == 'cliente':
                    return redirect('pagina_principal')

            return redirect('pagina_principal') 
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos. Por favor, vuelve a intentarlo.")
            return redirect('iniciar_sesion')
            
    return render(request, 'inicioSesion.html')


def perfil_comercio(request):
    if request.user.is_authenticated:
        # Buscamos qué tipo de usuario es la cuenta que inició sesión
        cuenta = Usuario.objects.filter(nombre_usuario=request.user.username).first()
        
        # Si es restaurante, lo mandamos a tu pantalla correcta de editar_perfil_comercio
        if cuenta and cuenta.tipo_usuario == 'restaurante':
            return redirect('perfil_comercio') 
        
    # Si es cliente o repartidor (o no está logueado), lo mandamos a la página principal
    return redirect('pagina_principal')

#vista para cerrar sesion
class CustomLogoutView(LogoutView):
    # Cuando termine de destruir la sesión, lo mandamos al login
    next_page = 'iniciar_sesion'