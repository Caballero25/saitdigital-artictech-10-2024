from django.shortcuts import render

# Create your views here.

def products_template(request):
    return render(request, 'ecommerce/products.html')
