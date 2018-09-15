# -*- coding: utf-8 -*-
'''
 Este programa descargará de forma automatica el archivo de texto comprimido
  en formato zip de RNC "DGII_RNC.zip" desde la url de la DGII.
  http://www.dgii.gov.do/app/WebApps/Consultas/rnc

 Creado por: Felix Ramirez
 Fecha: 04 Diciembre 2017
'''
import os
import zipfile
import requests


# Abrir conexion http...
def abrir_conexion(url):
    print('Abrir conexion %s' % url)
    response = requests.get(url, stream=True)

    return response


# Crear archivo local desde la lectura del archivo remoto - www
def hacer_descarga(archivo_local, archivo_remoto):
    url = 'http://www.dgii.gov.do/app/WebApps/Consultas/rnc/%s' % archivo_remoto

    respuesta = abrir_conexion(url)

    print('Descargando archvo "%s" a "%s", Espere...' %
          (archivo_remoto, archivo_local))

    with open(archivo_local, 'wb') as archivo_rnc:
        for paquete in respuesta.iter_content(chunk_size=1024):
            if paquete:
                archivo_rnc.write(paquete)

        print('Archivo "%s" descargado!' % archivo_local)


def descomprimir_archivo(arch_a_extraer, archivo_zip, ruta_destino):
    zip_ref = zipfile.ZipFile(archivo_zip)
    archivo_extraido = zip_ref.extract(arch_a_extraer, ruta_destino)

    return archivo_extraido


def abrir_archivo(archivo):
    cont = 0
    with open(archivo, 'r') as arch_rncs:
        for registro in arch_rncs:
            campos = registro.split('|')

            rnc = campos[0]               # 00103716205
            razon_social = campos[1]      # MARIA DE LOS ANGELES CASTILLO FERNANDEZ
            nombre_comercial = campos[2]  # COLMADO MARIA II
            tipo_negocio = campos[3]      # COLMADOS
            direccion_calle = campos[4]   # Null (MIGUEL ANGEL MONCLU NO 206)
            direccion_numero = campos[5]  # Null
            direccion_sector = campos[6]  # Null (MIRADOR NORTE)
            telefono = campos[7]          # Null (8093344620)
            fecha_ingreso = campos[8]     # Null (2011-02-02 11:16:42.553)
            estatus = campos[9]           # ACTIVO
            regimen = campos[10]          # NORMAL

            print(rnc, razon_social, nombre_comercial, tipo_negocio, direccion_calle, \
                  direccion_numero, direccion_sector, telefono, fecha_ingreso, \
                  estatus, regimen)
            cont += 1
            if cont == 10:
                break


if __name__ == '__main__':
    archivo_remoto = 'DGII_RNC.zip'
    arch_descargado = os.path.join(os.getcwd(), 'DGII_RNC.zip')
    arch_a_extraer = 'TMP/DGII_RNC.TXT'
    ruta_a_extraer = os.getcwd()

    hacer_descarga(arch_descargado, archivo_remoto)

    print('Descomprimiendo "%s", Espere...' % arch_descargado)

    arch_final = descomprimir_archivo(arch_a_extraer,
                                      arch_descargado,
                                      ruta_a_extraer)

    if arch_final:
        print('Archivo "%s", Descomprido' % arch_final)

    abrir_archivo(arch_final)
