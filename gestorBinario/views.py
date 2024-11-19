from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ArchivosCatalogo, Notificacion
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import smtplib
import random
import string
import os
import base64
# Create your views here.

@csrf_exempt
def codificar_archivo(request, id):
    #Verificamos que archivo debemos enviar al usuario
    if id == "1":
        #Offsets propuestos para cambiar el nombre
        offsets_list = [0x82E0 ,0x3E0, 0x81E0, 0x72E0]
        # Ruta del archivo .bin en la carpeta 'media'
        ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'FLASH_SM2TC1767_10SW0547001924V600-20240705-192259.bin')
    if id == "2":
        #Offsets propuestos para cambiar el nombre
        offsets_list = [0x200A0, 0x200E0, 0x21540, 0x21580, 0x292B0, 0x292F0, 0x2C630, 0x2C670, 0xA0, 0xE0, 0x10070, 0x100B0, ]
        # Ruta del archivo .bin en la carpeta 'media'
        ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'AIC_1AGWMAPP.bin')


    # Lee el contenido del archivo .bin
    with open(ruta_archivo, 'rb') as archivo:
        contenido_bin = archivo.read()
    if request.method == 'POST' and request.FILES['archivo']:
        archivo = request.FILES['archivo']
        if archivo:
            for offset in offsets_list:
                archivo.seek(offset)
                offset17 = archivo.read(17)
                offset17_ascii = offset17.decode('utf-8')
                if any(char.isalnum() for char in offset17_ascii):
                    print("offset legible")
                    contenido_base64 = base64.b64encode(contenido_bin).decode('utf-8')
                    #correo(request.user.username, request.user.email, nuevoArchivo.nombreAntiguo, nuevoArchivo.archivo.name)
                    return JsonResponse({
                        'nombre_archivo': offset17_ascii,
                        'contenido': contenido_base64
                    })
                else:
                    print("offset no legible")
                    continue

    
@login_required
def subirArchivoTemplate_1(request, id):
    if id == "1":
        #Nombre modulo 
        nombreModulo = 'Wingle7'
    elif id == "2":
        nombreModulo = 'POER'
    context = {"idArchivo": id,
                "nombre_modulo": nombreModulo
               }

    return render(request, "gestor/subirArchivo.html", context)

@login_required
def biblioteca(request): 
    archivos = ArchivosCatalogo.objects.filter(publico = True).order_by('-subido_en')
    context = {
        "archivos": archivos
    }
    return render(request, 'gestor/biblioteca.html', context)
    
    
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
