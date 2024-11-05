from django.urls import path
from .views import products_template, licenses_template

urlpatterns = [
    path('productos', products_template, name='products_template'),
    path('licencias', licenses_template, name='licenses_template'),
]