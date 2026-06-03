from django.shortcuts import render

# Create your views here.
def principal_restaurante(request):
    return render(request, 'principal_restaurante.html')
