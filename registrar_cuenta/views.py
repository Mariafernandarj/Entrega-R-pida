from django.shortcuts import render, redirect
from .models import Usuario

def seleccionar_tipo(request):
    return render(request, 'registrar_cuenta/seleccionar_tipo.html')

def formulario_registro(request, tipo):
    if tipo not in ['cliente', 'repartidor', 'restaurante']:
        return redirect('seleccionar_tipo')

    if request.method == 'POST':
        nombre = request.POST.get('nombre_usuario', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()
        confirmar = request.POST.get('confirmar_contrasena', '').strip()

        # Flujo alternativo: campos vacíos
        if not nombre or not contrasena or not confirmar:
            return render(request, 'registrar_cuenta/formulario.html', {
                'tipo': tipo,
                'error': 'Todos los campos son obligatorios.',
            })

        # Flujo alternativo: nombre ya registrado
        if Usuario.objects.filter(nombre_usuario=nombre).exists():
            return render(request, 'registrar_cuenta/formulario.html', {
                'tipo': tipo,
                'error': 'El nombre de usuario ya está registrado.',
            })

        # Flujo alternativo: contraseñas no coinciden
        if contrasena != confirmar:
            return render(request, 'registrar_cuenta/formulario.html', {
                'tipo': tipo,
                'error': 'Las contraseñas no coinciden.',
            })

        try:
            Usuario.objects.create(
                nombre_usuario=nombre,
                contrasena=contrasena,
                tipo_usuario=tipo,
            )
            return render(request, 'registrar_cuenta/formulario.html', {
                'tipo': tipo,
                'exito': True,
            })
        except Exception:
            # Flujo excepcional: falla del servidor
            return render(request, 'registrar_cuenta/formulario.html', {
                'tipo': tipo,
                'error': 'Error del servidor. Intenta de nuevo.',
            })

    return render(request, 'registrar_cuenta/formulario.html', {'tipo': tipo})

# Create your views here.
