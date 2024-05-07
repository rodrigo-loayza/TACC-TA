import re
from pypdf import PdfReader

# Fuente: Urin Qichwa VOCABULARIO PEDAGÓGICO QUECHUA SUREÑO
reader = PdfReader("urin.pdf")

# Secciones con oraciones útiles
pages_comm = reader.pages[17:47]  # Comunicación
pages_pers = reader.pages[60:68]  # Personal social y ciencias
pages_camp = reader.pages[109:131]  # Por campos semánticos

document = ""

### Sección Comunicación ###

# Regex patterns
pagination_pttrn = (
    r"Comunicación\nvocabulario\d+\sParte\sI\s-\sQuechua\ssureño"  # Datos de paginación
)
sentences_pttrn = r"\.[A-Za-z]?\s*[A-Za-z]?\s([^.]+\.)\s*‘([^‘’]+)’\."  # Grupo1 oración quechua, grupo2 oración español encerrada en ‘’

# Processing
for page in pages_comm:
    # Clean pagination
    text = re.sub(pagination_pttrn, "", page.extract_text())

    # Find quechua sentences
    matches = re.findall(sentences_pttrn, text)
    for m in matches:
        sentence = m[0].replace("\n", "")
        sentence = sentence.replace("/ ", "/")
        document += sentence + "\n"

### Sección Personal social y ciencias ###

# Regex patterns
pagination_pttrn = r"Personal\ssocial\sy\sCiencia\sy\stecnología\nvocabularioParte\sII\s-\sQuechua sureño\s\d+"  # Datos de paginación
sentences_pttrn = r"\.[A-Za-z]?\s*[A-Za-z]?\s([^.]+\.)\s*‘([^‘’]+)’\."  # Grupo1 oración quechua, grupo2 oración español encerrada en ‘’

# Processing
for page in pages_pers:
    # Clean pagination
    text = re.sub(pagination_pttrn, "", page.extract_text())

    # Find quechua sentences
    matches = re.findall(sentences_pttrn, text)
    for m in matches:
        sentence = m[0].replace("\n", "")
        sentence = sentence.replace("/ ", "/")
        document += sentence + "\n"

### Sección campos semánticos ###

# Regex patterns
pagination_pttrn = r"Palabras\spor\scampos\ssemánticos\sdel\squechua\ssureño\nUsadas\sen\sel\sárea\sde\sPersonal\ssocial\sy\sCiencia\sy\stecnologíaParte\sIII\s-\sQuechua\ssureño\s\d+"  # Datos de paginación
patron = r"([a-z].*?\.)\s*\n\s*((?:[A-Z].*?\.\s*)+)"  # Grupo1 oración en minúscula (palabras), grupo2 grupo de oraciones que empiezan en mayúsucula (ejemplos en quechua)

# Processing
for page in pages_camp:
    # Clean pagination
    text = re.sub(pagination_pttrn, "", page.extract_text())

    # Find quechua sentences
    matches = re.findall(patron, text, re.DOTALL)
    for m in matches:
        sentence = m[1].replace("\n", "")
        sentence = sentence.replace("/ ", "/")
        document += sentence + "\n"


corpus = {"documento": document, "variante": "unificada"}
print(corpus)
