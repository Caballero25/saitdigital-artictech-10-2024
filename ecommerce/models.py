from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)
    precio = models.FloatField()
    imagen_izquierda = models.ImageField(default=None)
    imagen_derecha_1 = models.ImageField(default=None)
    imagen_derecha_2 = models.ImageField(default=None)
    en_oferta = models.BooleanField(default=False)
    precio_oferta = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Licencia_Producto(models.Model):
    articulo = models.ForeignKey(Producto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    descripcion = RichTextField(config_name='producto')
    precio = models.FloatField()
    def __str__(self):
        return self.articulo.nombre +" | " +  self.descripcion[:20]