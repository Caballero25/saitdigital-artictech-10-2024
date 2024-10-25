from django.db import models

# Create your models here.

class ArchivoBinarioChangeName(models.Model):
    nombreAntiguo = models.CharField(max_length=255)  # Nombre opcional para el archivo
    offset0x3E0 = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='copias/')#, blank=True, null=True, default='copias/x/FLASH_SM2TC1767_10SW0547001924V600-20240705-192259.bin')
    subido_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.archivo.name


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
    
class ArchivoUnico(models.Model):
    archivoUnico = models.FileField(upload_to='x/')