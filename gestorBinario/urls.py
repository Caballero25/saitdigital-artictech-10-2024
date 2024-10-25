from django.urls import path
from .views import *

urlpatterns = [
    path('subirArchivo', subirArchivo, name="subirArchivo"),
    path('subirArchivoBinario', subirArchivoTemplate, name="subirArchivoTemplate"),
    path('catalogoArchivos', catalogoArchivos, name="catalogoArchivos"),
    path('correo', correo)
]


