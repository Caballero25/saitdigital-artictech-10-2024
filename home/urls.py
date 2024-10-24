from django.urls import path
from .views import home, userLogin, logout_view

urlpatterns = [
    path('', home, name='home-url'),
    path('login', userLogin, name='login-url'),
    path('logout', logout_view, name='logout-url'),
]


