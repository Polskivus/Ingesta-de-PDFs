SEPARADORES =  ["\n\n", "\n", ".", " "]

def crear_chunks(pagina, metodo, texto):
    return {
        "documento": pagina["documento"],
        "pagina": pagina["pagina"],
        "origen": pagina["origen"],
        "metodo": metodo,
        "texto": texto
    }

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

def chunk_recursive(paginas, size=500):
    chunks = []
    for p in paginas:
        trozos = dividir_recursivo(p["texto"], size, SEPARADORES)
        for texto in agrupar(trozos, size):
            texto = texto.strip()
            if texto:
                chunks.append(crear_chunks(p, "recursive", texto))
    return chunks