from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Producto, Licencia, Descripcion_Producto, Descripcion_Licencia

# Create your views here.

def products_template(request):
    queryset = Producto.objects.filter(disponible=True)  # Obtén el queryset
    paginator = Paginator(queryset, 6)  # 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ecommerce/products.html', {'page_obj': page_obj})


def licenses_template(request):
    queryset = Licencia.objects.filter(disponible=True)  # Obtén el queryset
    paginator = Paginator(queryset, 6)  # 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ecommerce/licenses.html', {'page_obj': page_obj})

def detail_template(request, tipo, id):
    print(tipo)
    if tipo == 'producto':
        producto = Producto.objects.filter(disponible=True, pk=id).first()
        descripciones = Descripcion_Producto.objects.filter(articulo=producto).all()
        return render(request, 'ecommerce/detail.html', {'producto': producto, "descripciones": descripciones})
    if tipo == 'licencia':
        producto = Licencia.objects.filter(disponible=True, pk=id).first()
        descripciones = Descripcion_Licencia.objects.filter(articulo=producto).all()
        return render(request, 'ecommerce/detail.html', {'producto': producto, "descripciones": descripciones})