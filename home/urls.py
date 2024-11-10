from django.urls import path
from .views import home, userLogin, logout_view, our_services, about_us

urlpatterns = [
    path('', home, name='home-url'),
    path('login', userLogin, name='login-url'),
    path('logout', logout_view, name='logout-url'),
    path('servicios', our_services, name='our_services_url'),
    path('nosotros', about_us, name='about_us_url'),
]


