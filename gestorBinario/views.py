from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ArchivoBinarioChangeName, ArchivosCatalogo, Notificacion, ArchivoUnico
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import smtplib
import random
import string
import os
# Create your views here.

@csrf_exempt
def subirArchivo(request):
    if request.method == 'POST' and request.FILES['archivo']:
        archivo = request.FILES['archivo']
        if archivo:
            archivo.seek(0x3E0)
            offset3E0 = archivo.read(17)
            try:
                offset3E0_ascii = offset3E0.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    offset3E0_ascii = offset3E0.decode('latin-1')
                except UnicodeDecodeError:
                    offset3E0_ascii = offset3E0.hex()
            try:
                archivoUnic = ArchivoUnico.objects.filter(archivoUnico__contains="ASH_SM2TC1767_10SW0547001924V600-202407").first()
                archivoX = archivoUnic.archivoUnico
                directorio_destino = os.path.join(settings.MEDIA_ROOT, 'copias')
                fs = FileSystemStorage(location=directorio_destino)
                nombre_archivo = fs.save(auditarNombreArchivo(offset3E0_ascii)+".bin", archivoX)
                print(nombre_archivo)
            except:
                print(8)
                return JsonResponse({'error': 'No se pudo emcontrar el archivo'}, status=400)
            nuevoArchivo = ArchivoBinarioChangeName.objects.create(
                nombreAntiguo=str(archivoUnic.archivoUnico.name),
                offset0x3E0=offset3E0_ascii,
                archivo="copias/"+nombre_archivo
            )
            nuevoArchivo.save()
            archivo_url = nuevoArchivo.archivo.url
            print("archivo url" + archivo_url)
            correo(request.user.username, request.user.email, nuevoArchivo.nombreAntiguo, nuevoArchivo.archivo.name)
            return JsonResponse({'mensaje': 'Archivo subido con éxito', 'archivo_url': archivo_url, 'nuevoNombre': nuevoArchivo.offset0x3E0})
    return JsonResponse({'error': 'No se pudo subir el archivo'}, status=400)

    
@login_required
def subirArchivoTemplate(request):
    return render(request, "gestor/subirArchivo.html")

@login_required
def catalogoArchivos(request): 
    archivos = ArchivosCatalogo.objects.filter(publico = True).order_by('-subido_en')
    context = {
        "archivos": archivos
    }
    return render(request, 'catalogoArchivos.html', context)
def auditarNombreArchivo(renombrar):
    existeNombre = ArchivoBinarioChangeName.objects.filter(Q(nombreAntiguo=renombrar) | Q(offset0x3E0 = renombrar)).first()
    if existeNombre:
        editNombre = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
        existeNombreRandomx2 = ArchivoBinarioChangeName.objects.filter(Q(nombreAntiguo=(renombrar + editNombre)) | Q(offset0x3E0 = (renombrar + editNombre))).first()
        if existeNombreRandomx2:
            auditarNombreArchivo(existeNombreRandomx2)
        else:
            return renombrar + editNombre
    else:
        return renombrar
    
    
    
def correo(nombreUsuario, correoUsuario, nombreAntiguoArchivo, nombreNuevoArchivo):
    if correoUsuario == "" or correoUsuario == None:
        correoUsuario = "SIN CORREO ASIGNADO"
    try:
        mensaje = f"""
            El usuario {nombreUsuario} con correo {correoUsuario} utilizó el sistema. \n
            Archivo subido: {nombreAntiguoArchivo}\n
            Archivo entregado por el sistema: {nombreNuevoArchivo}
        """
        correo_electronico = 'davidcame124@gmail.com'
        asunto = "Un usuario utilizó el sistema de archivos binarios"

        body = 'Subject: {}\n\n{}'.format(asunto, mensaje)
        server = smtplib.SMTP('smtp.gmail.com','587')
        server.starttls()
        server.login('artcictechsystem@gmail.com','password')
        server.sendmail('artcictechsystem@gmail.com', correo_electronico, body.encode('utf-8'))
        server.quit()
    except:
        try:
            mensaje = f"""
                El usuario {nombreUsuario} con correo {correoUsuario} utilizó el sistema. \n
                Archivo subido: {nombreAntiguoArchivo}\n
                Archivo entregado por el sistema: {nombreNuevoArchivo}
            """
            new_notificacion = Notificacion.objects.create(mensaje=mensaje)
            new_notificacion.save()
        except:
            print("Ocurrió un error inesperado")
