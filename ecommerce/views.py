from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Producto

# Create your views here.

def products_template(request):
    queryset = Producto.objects.filter(disponible=True)  # Obtén el queryset
    paginator = Paginator(queryset, 6)  # 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ecommerce/products.html', {'page_obj': page_obj})


def licenses_template(request):
    queryset = Producto.objects.filter(disponible=True)  # Obtén el queryset
    paginator = Paginator(queryset, 6)  # 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ecommerce/licenses.html', {'page_obj': page_obj})
