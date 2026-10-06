from extraer import extraer_documento
from chunkers import chunk_fixed, chunk_overlap, chunk_recursive, chunk_structure

paginas = extraer_documento("prueba.pdf")

for nombre, funcion in [("fixed", chunk_fixed), ("overlap", chunk_overlap), ("recursive", chunk_recursive), ("structure", chunk_structure)]:
    chunks = funcion(paginas)
    longitudes = [len(c["texto"]) for c in chunks]
    print(f"=== {nombre}: {len(chunks)} chunks (mín {min(longitudes)}, máx {max(longitudes)}) ===")
    for c in chunks[:3]:
        print(f"[pág {c['pagina']}] {c['texto']!r}")
        print()