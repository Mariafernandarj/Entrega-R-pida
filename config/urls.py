from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('core.urls')),
    path('inicioSesion/', include('inicio_sesion.urls')),
    path('busqueda/', include('busqueda_restaurante_comida.urls')),
    path('compra/', include('hacer_compra.urls')),
    path('comercio/', include('editar_perfil_comercio.urls')),
    #apunta a la carpeta
    path('', include('registrar_cuenta.urls')),
    path('', include('solicitudes_reparto.urls')),
    path('', include('navegar_menus.urls')),
    path('', include('principal_repartidor.urls')),
    path('', include('principal_restaurante.urls')),
    path('', include('solicitudes_restaurante.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
