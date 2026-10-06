import re

SEPARADORES =  ["\n\n", "\n", ".", " "]
PATRON_TITULO = re.compile(
    r"^(\d+(\.\d+)*\.?\s+\S.*|[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9 ,:\-]{3,}$)"
)

# Funciones auxiliares
def crear_chunks(pagina, metodo, texto):
    return {
        "documento": pagina["documento"],
        "pagina": pagina["pagina"],
        "origen": pagina["origen"],
        "metodo": metodo,
        "texto": texto
    }

def dividir_recursivo(texto, size, separadores):
    if len(texto) <= size:
        return[texto]
    if not separadores:
        return [texto[i:i + size] for i in range(0, len(texto), size)]

    separador, resto = separadores[0], separadores[1:]
    partes = texto.split(separador)
    trozos = []
    for i, parte in enumerate(partes):
        if i < len(partes) - 1:
            parte += separador
        trozos.extend(dividir_recursivo(parte, size, resto))
    return trozos

def agrupar(trozos, size):
    chunks, actual = [], ""
    for trozo in trozos:
        if len(actual) + len(trozo) <= size:
            actual += trozo
        else:
            if actual:
                chunks.append(actual)
                actual = trozo
    if actual:
        chunks.append(actual)
    return chunks

def _linea_tabla(linea):
    return bool(re.search(r"\S {3,}\s", linea))

def _es_titulo(linea):
    l = linea.strip()
    return len(l) <= 80 and not l.endswith(".") and bool(PATRON_TITULO.match(l))

def _bloques(texto):
    bloques, tipo, lineas = [], None, []

    def cerrar():
        nonlocal tipo, lineas
        if lineas:
            bloques.append((tipo, "\n".join(lineas)))
        tipo, lineas = None, []

    for linea in texto.splitlines():
        if not linea.strip():
            cerrar()
            continue
        if _linea_tabla(linea):
            nuevo = "tabla"
        elif _es_titulo(linea):
            nuevo = "titulo"
        else:
            nuevo = "texto"
        if nuevo != tipo or nuevo == "titulo":
            cerrar()
            tipo = nuevo
        lineas.append(linea.strip() if nuevo == "titulo" else linea)
    cerrar()
    return bloques

def _secciones(bloques):
    secciones, titulo, contenido = [], "", []
    for tipo, texto in bloques:
        if tipo == "titulo":
            if titulo or contenido:
                secciones.append((titulo, contenido))
            titulo, contenido = texto, []
        else:
            contenido.append((tipo, texto))
    if titulo or contenido:
        secciones.append((titulo, contenido))
    return secciones

# Para hacer chunking fixed
def chunk_fixed(paginas, size=500):
    chunks = []
    for p in paginas:
        texto = p["texto"]
        for i in range(0, len(texto), size):
            chunk = texto[i:i + size].strip()
        if chunk:
            chunks.append(crear_chunks(p, "fixed", chunk))
    return chunks

def chunk_overlap(paginas, size=500, solape=100):
    paso = size - solape
    chunks = []
    for p in paginas:
        texto = p["texto"]
        for i in range(0, len(texto), paso):
            chunk = texto[i:i + size].strip()
            if chunk:
                chunks.append(crear_chunks(p, "overlap", chunk))
            if i + size >= len(texto):
                break
    return chunks

def chunk_recursive(paginas, size=500):
    chunks = []
    for p in paginas:
        trozos = dividir_recursivo(p["texto"], size, SEPARADORES)
        for texto in agrupar(trozos, size):
            texto = texto.strip()
            if texto:
                chunks.append(crear_chunks(p, "recursive", texto))
    return chunks

def chunk_structure(paginas, size=1000):
    chunks = []
    for p in paginas:
        for titulo, contenido in _secciones(_bloques(p["texto"])):
            partes = [titulo] if titulo else []
            partes += [t for tipo, t in contenido if tipo == "texto"]
            texto_seccion = "\n\n".join(partes).strip()
            if texto_seccion:
                trozos = dividir_recursivo(texto_seccion, size, SEPARADORES)
                for trozo in agrupar(trozos, size):
                    if trozo.strip():
                        chunks.append(crear_chunks(p, "structure", trozo.strip()))
            for tipo, t in contenido:
                if tipo == "tabla":
                    chunks.append(crear_chunks(p, "structure", (titulo + "\n" + t).strip()))
    return chunks