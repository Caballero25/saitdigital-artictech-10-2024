from django.urls import path
from .views import subirArchivoTemplate_1, biblioteca, codificar_archivo

urlpatterns = [
    path('subirArchivo/<str:id>', codificar_archivo, name="subirArchivoUno"),
    path('subir-archivo/<str:id>', subirArchivoTemplate_1, name="subirArchivoTemplate_1"),
    path('biblioteca', biblioteca, name="biblioteca-url"),
]


