from django.shortcuts import render, redirect

def principal_restaurante(request):
    # 👇 Candado: Si no está autenticado, lo rebota al login inmediatamente
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')
        
    return render(request, 'principal_restaurante.html')