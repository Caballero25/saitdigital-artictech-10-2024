from django.db import models

# Create your models here.

class ArchivosCatalogo(models.Model):
    publico = models.BooleanField(null=False, blank=False)
    archivo = models.FileField(upload_to='catalogo/')
    subido_en = models.DateTimeField(auto_now_add=True)
    subido_por = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.subido_por
    def save(self, *args, **kwargs):
        if not self.pk and 'user' in kwargs:
            self.subido_por = kwargs.pop('user').username
        super().save(*args, **kwargs)
        
class Notificacion(models.Model):
    mensaje = models.TextField(max_length=200)
    subido = models.DateTimeField(auto_now_add=True)
    