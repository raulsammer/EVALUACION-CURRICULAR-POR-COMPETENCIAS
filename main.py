#created by Raul Sammer Quispe Lozano
#Mas info: raulito.xyz 

import os
import fitz
import docx
from unidecode import unidecode
import matplotlib.pyplot as plt
import numpy as np

# Función para calcular el porcentaje de coincidencia
def calcular_porcentaje_coincidencia(texto, palabras_compendio):
    palabras_encontradas = {}
    palabras_totales = len(texto.split())

    # Convertir el texto a minúsculas y quitar tildes
    texto = unidecode(texto.lower())

    for palabra in texto.split():
        # Convertir la palabra a minúsculas y quitar tildes antes de la comparación
        palabra = unidecode(palabra.lower())
        if palabra in palabras_compendio:
            palabras_encontradas[palabra] = palabras_encontradas.get(palabra, 0) + 1

    return (palabras_encontradas, (len(palabras_encontradas) / palabras_totales) * 100)

# Carpeta que contiene los archivos SILABUS
carpeta_silabus = "SILABUS"

# Leer el archivo de compendio y almacenar las palabras en un diccionario
compendio = {}
with open('compendio-solo.txt', 'r') as compendio_file:
    lineas = compendio_file.readlines()
    encabezado_actual = None
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("-"):
            encabezado_actual = linea[1:]
            compendio[encabezado_actual] = []
        elif encabezado_actual:
            compendio[encabezado_actual].append(linea)

# Recorrer los archivos en la carpeta SILABUS
for archivo in os.listdir(carpeta_silabus):
    if archivo.endswith(".pdf") or archivo.endswith(".docx"):
        ruta_archivo = os.path.join(carpeta_silabus, archivo)
        contenido = ""

        # Leer el contenido del archivo PDF o DOCX
        if archivo.endswith(".pdf"):
            pdf_document = fitz.open(ruta_archivo)
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                contenido += page.get_text()
        elif archivo.endswith(".docx"):
            doc = docx.Document(ruta_archivo)
            for paragraph in doc.paragraphs:
                contenido += paragraph.text

        # Calcular el porcentaje de coincidencia para cada encabezado
        resultados_encabezado = {}
        campos_cero_porcentaje = []  # Para almacenar campos con 0.00%
        for encabezado, palabras in compendio.items():
            palabras_encontradas, porcentaje = calcular_porcentaje_coincidencia(contenido, palabras)
            if porcentaje > 0.00:
                resultados_encabezado[encabezado] = porcentaje
            else:
                campos_cero_porcentaje.append(encabezado)

        # Crear un gráfico de pastel si hay datos para graficar
        if resultados_encabezado:
            fig, ax = plt.subplots()
            labels = resultados_encabezado.keys()
            sizes = resultados_encabezado.values()

            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

            # Agregar etiqueta especial para campos con 0.00%
            if campos_cero_porcentaje:
                etiqueta_cero = "\nNota: Campos con 0% en " + archivo + " son: " + ", ".join(campos_cero_porcentaje)
                ax.annotate(etiqueta_cero, xy=(1, 0), xytext=(10, -200), textcoords='offset points',
                            fontsize=10, color='black', ha='right', va='bottom')

            plt.title(f'{archivo}')

            # Guardar el gráfico en el sistema de archivos
            plt.savefig(f'{archivo}_grafico_pie.png', bbox_inches='tight')

            # Mostrar el gráfico
            plt.show()
