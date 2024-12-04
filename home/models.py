from django.db import models

# Create your models here.

class Ofertas_Usuario(models.Model):
    aviso = models.TextField(max_length=100, blank=False, null=False)
    publico = models.BooleanField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.aviso[:35] + "..."