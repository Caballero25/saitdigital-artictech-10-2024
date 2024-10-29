from django.urls import path
from .views import products_template

urlpatterns = [
    path('productos', products_template, name='products_template')
]