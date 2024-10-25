from django.urls import path
from .views import subirArchivoTemplate_1, catalogoArchivos, codificar_archivo

urlpatterns = [
    #path('subirArchivo', subirArchivo, name="subirArchivo"),
    path('subirArchivo/<str:id>', codificar_archivo, name="subirArchivoUno"),
    path('subir-archivo/<str:id>', subirArchivoTemplate_1, name="subirArchivoTemplate_1"),
    path('catalogoArchivos', catalogoArchivos, name="catalogoArchivos"),
]


