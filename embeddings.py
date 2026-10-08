import os
import numpy as np
import ollama
from dotenv import load_dotenv

load_dotenv()

client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
MODELO = "bge-m3"
DIM = 1024

textos = ["Esto es una prueba", "This is a test"]

def embed(textos, lote=32):
    vectores = []
    for i in range(0, len(textos), lote):
        resp = client.embed(model=MODELO, input=textos[i:i + lote])
        vectores.extend(resp["embeddings"])
    return np.array(vectores, dtype=np.float32)

print(embed(textos))
