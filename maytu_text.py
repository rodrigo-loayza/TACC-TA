
import PyPDF2

def extraer_lineas(inicio, fin, pdf_path, tipo):
    paginas = []

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_paginas = len(reader.pages)

        for pagina_num in range(inicio,fin+1):
            pag = []
            pagina = reader.pages[pagina_num]
            contenido = pagina.extract_text()

            # Dividir el contenido de la página en lineas
            palabras = contenido.split('\n')
            #si la linea empieza con digito, entonces se elimina ese digito que es el indicador de pagina
            if palabras[0].isdigit():
              del palabras[0]
            else:
              #si la linea es el comienzo de un capitulo, el titulo se guardó al ultimo y se procede a eliminarlo
              del palabras[-5:]

            #une las palabras en una linea
            pag.append(" ".join(palabras))

            #añade las lineas a el texto completo divido por paginas
            paginas.append(" ".join(pag[0].split()))

    #une todo el texto y regresa un diccionario
    return dict([('Texto', " ".join(paginas)), ('Tipo de fuente', tipo)])

paginas = extraer_lineas(8,158, "quehcua chanka.pdf", "Chanka")

paginas
