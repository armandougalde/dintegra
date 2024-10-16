import pdfplumber

def extraer_imagenes_de_pdf(pdf_file):
    # Abrimos el archivo PDF
    with pdfplumber.open(pdf_file) as pdf:
        # Extraemos la primera página
        primera_pagina = pdf.pages[0]
        # Convertimos la página a una imagen
        imagen = primera_pagina.to_image()
        imagen_path = "pagina_1.jpg"
        imagen.original.save(imagen_path)  # Guardamos la imagen en un archivo
        print(f"Imagen guardada en: {imagen_path}")

# Prueba cargando el archivo PDF manualmente
extraer_imagenes_de_pdf("C:/Users/arman/Downloads/ZNIL.pdf")



import pdfplumber
from PIL import ImageEnhance

def extraer_imagen_con_resolucion(pdf_file_path, dpi=300):
    with pdfplumber.open(pdf_file_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # Extraemos la página como imagen, especificando una resolución mayor (dpi)
            im = page.to_image(resolution=dpi).original

            # Puedes mejorar el contraste de la imagen para ayudar al OCR
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(2)  # Ajustar el valor según lo necesites

            # Guardamos la imagen procesada
            imagen_path = f"pagina_{page_number + 1}_resolucion_mejorada.jpg"
            im.save(imagen_path)
            print(f"Imagen de la página {page_number + 1} guardada en: {imagen_path}")

# Llamar a la función con el archivo PDF y aumentar la resolución
extraer_imagen_con_resolucion(r'C:/Users/arman/Downloads/ZNIL.pdf', dpi=1200)