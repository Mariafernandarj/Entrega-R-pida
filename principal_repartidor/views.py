from django.shortcuts import render

# Create your views here.
def principal_repartidor(request):
    return render(request, 'principal_repartidor.html')
