from django import forms
from .models import ArchivosCatalogo

class ArchivosCatalogoForm(forms.ModelForm):
    class Meta:
        model = ArchivosCatalogo
        fields = ['archivo', 'publico'] # Lista los campos que quieres mostrar y editar en el admin