import re
from pypdf import PdfReader

# Fuente: Urin Qichwa VOCABULARIO PEDAGÓGICO QUECHUA SUREÑO
reader = PdfReader("urin.pdf")
pages = reader.pages[17:42]  # Vocabulary start

# Regex patterns
pagination_pttrn = (
    r"Comunicación\nvocabulario\d+\sParte\sI\s-\sQuechua\ssureño"  # Datos de paginación
)
sentences_pttrn = r"\.[A-Za-z]?\s*[A-Za-z]?\s([^.]+\.)\s*‘([^‘’]+)’\."  # Grupo1 oración quechua, grupo2 oración español encerrada en ‘’

communication_txt = ""
for page in pages:
    # Clean pagination
    text = re.sub(pagination_pttrn, "", page.extract_text())

    # Find quechua sentences
    matches = re.findall(sentences_pttrn, text)
    for m in matches:
        sentence = m[0].replace("\n", "")
        sentence = sentence.replace("/ ", "/")
        communication_txt += sentence + "\n"

corpus = {"documento": communication_txt, "variante": "unificada"}
print(corpus)
