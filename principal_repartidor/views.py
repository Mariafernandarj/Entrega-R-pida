from django.shortcuts import render, redirect

def principal_repartidor(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')
    return render(request, 'principal_repartidor.html')