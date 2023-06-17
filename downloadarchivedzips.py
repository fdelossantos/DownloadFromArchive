### DownloadFromArchive
### Proyecto de aprendizaje que permite descargar una colección desde Archive.org.
### Licencia: GNU General Public License v3.0.
### Author: federicod (twitter), fdelossantos (GitHub)

from urllib.parse import unquote
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import re
import os  


# Constantes
site_url = "https://archive.org"

def abrir_resultado(url, destination):
    responseR = requests.get(url)
    soupR = BeautifulSoup(responseR.content, 'html.parser')
    zipslinks = soupR.find_all(href=re.compile('_jp2.zip'))
    
    if len(zipslinks) > 0:
        zip_url = site_url +  zipslinks[0]['href']
        quotedFilename = zip_url.split('/')[-1]
        realFileName = unquote(quotedFilename)
        print(f"Descargando {realFileName}...")
        savePath = destination + "\\" + realFileName
        urlretrieve(zip_url, savePath)

        print(f"Descarga del archivo {realFileName} completada en {destination}.")
        return True
    
    return False


def abrir_pagina_resultado(path, page, base, destino):
    response = requests.get(base + path + f"?page={page}")
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all(href=re.compile(f"({path}_)"))
    descargados = 0
    for link in links:
        print(base + link['href'])
        if abrir_resultado(base + link['href'], destino):
            descargados += 1
    return descargados


def recorrer_resultados_busqueda(base_url:str, desde:int, hasta:int, salvar_a:str):
    for pagina in range(desde, hasta+1):
        page_url = f"{base_url}?page={pagina}"
        print(f"Procesando página {pagina} - URL: {page_url}")
        desc = abrir_pagina_resultado(base_url, pagina, site_url,salvar_a)
    print(f"Se descargaron {desc} archivos.")
    return


print("Este script le permite descargar archivos zip originales de una colección de Archive.org.")
print("Úselo con criterio. El programa no está completamente probado, es tan solo un proyecto personal para aprender python.")
print("El programa no tiene ninguna garantía implícita ni explícita. Usted asume la responsabilidad de usuarlo.")
print("Aplica la licencia: GNU General Public License v3.0")
strUrl = input("Ingrese la URL base de descarga (/details/<nombre-archivo>):  ")
inicio = int(input("Ingrese el número de página inicial: "))
fin = int(input("Ingrese el número de página final: "))
carpetaDestino = input("Ingrese la carpeta de destino (c:\\temp): ")
if (strUrl == ""):
    print(f"La ruta que ingresó está vacía.")
    exit()
if not os.path.exists(carpetaDestino):
    print(f"La ruta '{carpetaDestino}' no es válida. Debe crearla previamente.")
    exit()
recorrer_resultados_busqueda(strUrl, inicio, fin, carpetaDestino)
print("El programa ha terminado.")