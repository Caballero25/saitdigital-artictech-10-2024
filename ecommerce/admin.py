from django.contrib import admin
from .models import Producto, Licencia, Descripcion_Licencia, Descripcion_Producto
# Register your models here.


admin.site.register(Producto)
admin.site.register(Licencia)
admin.site.register(Descripcion_Licencia)
admin.site.register(Descripcion_Producto)