from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'index.html')

def our_services(request):
    return render(request, 'landing/our_services.html')

def about_us(request):
    return render(request, 'landing/about_us.html')

def userLogin(request):
    context = {}
    if request.method == "GET":
        return render(request, "user/login.html", context)
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        userAuth = authenticate(request, username=username, password=password)
        if userAuth:
            login(request, userAuth)
            return redirect('home-url')
        else:
            context['error'] = "Credenciales Incorrectas, por favor, solicite soporte."
            return render(request, "user/login.html", context)
        
def logout_view(request):
    logout(request)
    return redirect('home-url')