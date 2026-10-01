import os
import subprocess
import tempfile
import re

from pypdf import PdfReader
from PIL import Image
import pytesseract

MIN_CHAR = 50 # Con esto decidimos el metodo de extraccion de información

def limpiar_layout(texto):
    texto = re.sub(r"\.{4,}", " ", texto)
    lineas = [re.sub(r"[ \t]+$", "", linea) for linea in texto.splitlines()]
    texto = "\n".join(lineas)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()

def ocr_pagina(ruta_pdf, numero):
    with tempfile.TemporaryDirectory() as tmp:
        prefijo = os.path.join(tmp, "pagina")
        subprocess.run(
            ["pdftoppm", "-r", "300", "-png", "-f", str(numero), "-l", str(numero), "-singlefile", ruta_pdf, prefijo],
            check=True,
        )
        imagen = Image.open(prefijo + ".png")
        return pytesseract.image_to_string(imagen, lang="spa")

def extraer_documento(ruta_pdf):
    lector = PdfReader(ruta_pdf)
    paginas = []
    for numero, pagina in enumerate(lector.pages, start=1):
        texto = limpiar_layout(pagina.extract_text(extraction_mode="layout") or "")
        origen = "texto"
        if len("".join(texto.split())) < MIN_CHAR:
            texto = ocr_pagina(ruta_pdf, numero).strip()
            origen = "ocr"
        paginas.append({
            "documento": os.path.basename(ruta_pdf),
            "pagina": numero,
            "origen": origen,
            "texto": texto,
        })
    return paginas

if __name__ == "__main__":
    for p in extraer_documento("prueba.pdf"):
        print(f"--- Pagina {p['pagina']} ({p['origen']}, {len(p['texto'])} caracteres) ---")
        print(p["texto"][:200].replace("\n", " "))
        print()