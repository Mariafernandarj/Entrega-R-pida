from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('core.urls')),
    path('inicioSesion/', include('inicio_sesion.urls')),
    path('busqueda/', include('busqueda_restaurante_comida.urls')),
    path('compra/', include('hacer_compra.urls')),
    path('comercio/', include('editar_perfil_comercio.urls')),
] #apunta a la carpeta
    path('', include('registrar_cuenta.urls')),
    path('', include('solicitudes_reparto.urls')),
]
