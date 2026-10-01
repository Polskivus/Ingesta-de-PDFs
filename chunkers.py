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

def chunk_overlapse(paginas, size=500, solape=100):
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