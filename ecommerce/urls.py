from django.urls import path
from .views import products_template, detail_template

urlpatterns = [
    path('productos', products_template, name='products_template'),
    path('detalle/<str:tipo>/<str:id>', detail_template, name='detail_template'),
]