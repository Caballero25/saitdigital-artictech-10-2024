from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ArchivosCatalogo, Notificacion
import smtplib
import os
import base64
import re
# Create your views here.

@csrf_exempt
def codificar_archivo(request, id):
    #Verificamos que archivo debemos enviar al usuario
    if id == "1":
        #Offsets propuestos para cambiar el nombre
        offsets_list = [0x82E0 ,0x3E0, 0x81E0, 0x72E0]
        # Ruta del archivo .bin en la carpeta 'media'
        ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'FLASH_SM2TC1767_10SW0547001924V600-20240705-192259.bin')
        #Nombre del módulo
        nombre_modulo = "Wingle_7"
    if id == "2":
        #Offsets propuestos para cambiar el nombre
        offsets_list = [0x200A0, 0x200E0, 0x21540, 0x21580, 0x292B0, 0x292F0, 0x2C630, 0x2C670, 0xA0, 0xE0, 0x10070, 0x100B0, ]
        # Ruta del archivo .bin en la carpeta 'media'
        #ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'AIC_1AGWMAPP.bin')
        ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'V2_OPTIMIZACION.bin')
        #Nombre del módulo
        nombre_modulo = "POER"


    # Lee el contenido del archivo .bin
    with open(ruta_archivo, 'rb') as archivo:
        contenido_bin = archivo.read()
    if request.method == 'POST' and request.FILES['archivo']:
        archivo = request.FILES['archivo']
        contenido_subido = archivo.read()
        patrones = ["8L4", "LGW"]
        resultado = buscar_palabras_binario(contenido_subido, patrones)
        if resultado:
            print(resultado)
        if archivo:
            print(str(archivo))
            if resultado and len(resultado) > 2:
                print("offset legible")
                contenido_base64 = base64.b64encode(contenido_bin).decode('utf-8')
                correo(request.user.username, request.user.email, nombre_modulo, str(archivo), str(resultado))
                return JsonResponse({
                    'nombre_archivo': resultado,
                    'contenido': contenido_base64
                })
            else:
                print("offset no legible")
                

    
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
    
    
def correo(nombreUsuario, correoUsuario, nombre_modulo, archivo_subido, offset):
    print(f"Archivo subido: {archivo_subido} | Archivo entregado: {offset}")
    if correoUsuario == "" or correoUsuario == None:
        correoUsuario = "SIN CORREO ASIGNADO"
    try:
        mensaje = f"""
            El usuario {nombreUsuario} con correo {correoUsuario} utilizo el sistema. \n
                Modulo utilizado: {nombre_modulo}\n
                Archivo subido por el cliente fue: {archivo_subido} \n
                Nombre de archivo entregado por el sistema fue: {offset}.bin \n
        """
        correo_electronico = 'soport@art-ic.tech'
        asunto = f"Un usuario utilizó el sistema | {nombre_modulo}"

        body = 'Subject: {}\n\n{}'.format(asunto, mensaje)
        server = smtplib.SMTP('smtp.gmail.com','587')
        server.starttls()
        server.login('artcictechsystem@gmail.com','')
        server.sendmail('artcictechsystem@gmail.com', correo_electronico, body.encode('utf-8'))
        server.quit()
    except:
        try:
            mensaje = f"""
                El usuario {nombreUsuario} con correo {correoUsuario} utilizo el sistema. \n
                Modulo utilizado: {nombre_modulo}\n
                Archivo subido por el cliente fue: {archivo_subido} \n
                Nombre de archivo entregado por el sistema fue: {offset}.bin \n

                <h1>HOLA MUNDO</h1>
            """
            new_notificacion = Notificacion.objects.create(mensaje=mensaje)
            new_notificacion.save()
        except:
            print("Ocurrió un error inesperado")

def buscar_palabras_binario(contenido_binario, patrones, longitud_palabra=17):
        palabra_final = ""
        for i in range(len(contenido_binario) - longitud_palabra + 1):
            posible_palabra = contenido_binario[i:i + longitud_palabra].decode("utf-8", errors="ignore")
            if any(posible_palabra.startswith(p) for p in patrones):
                palabra_final = posible_palabra  # Almacena la última palabra encontrada
        return palabra_final