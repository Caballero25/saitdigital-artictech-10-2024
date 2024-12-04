from .models import Ofertas_Usuario  

def avisos_usuario_context(request):
    avisosUsuario = Ofertas_Usuario.objects.filter(publico=True).order_by('-updated_at')[:5]  # Ajusta según el número de notificaciones que deseas mostrar
    return {
        'AvisosUsuario': avisosUsuario
    }
