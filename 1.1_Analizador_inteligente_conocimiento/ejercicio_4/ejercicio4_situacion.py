import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path="../.env")

CARPETA_SALIDA = "."
MODELO = "gpt-4o-mini"
DOCUMENTO_PDF = "documento.pdf"

client = OpenAI()
path_pdf = DOCUMENTO_PDF if os.path.exists(DOCUMENTO_PDF) else os.path.join("..", DOCUMENTO_PDF)

def obtener_file_id(client, path_pdf):
    ruta_cache = "file_id.txt" if os.path.exists("file_id.txt") else os.path.join("..", "file_id.txt")
    if os.path.exists(ruta_cache):
        with open(ruta_cache, "r", encoding="utf-8") as f:
            file_id = f.read().strip()
        print(f"Reutilizando File ID existente: {file_id}")
        return file_id
    else:
        print(f"Subiendo PDF por primera vez: {path_pdf}...")
        archivo = client.files.create(file=open(path_pdf, "rb"), purpose="user_data")
        file_id = archivo.id
        with open(ruta_cache, "w", encoding="utf-8") as f:
            f.write(file_id)
        print(f"PDF subido. File ID guardado en {ruta_cache}: {file_id}")
        return file_id

file_id = obtener_file_id(client, path_pdf)

situacion_usuario = input("Escribe tu situación personal: ").strip()
contexto_opcional = input("Contexto opcional (Enter para omitir): ").strip()

prompt = f"""
Analiza según el PDF adjunto:
- Situación: "{situacion_usuario}"
- Contexto: "{contexto_opcional}"

Si el PDF no contiene información suficiente, 'encontrado_en_documento' debe ser false y la recomendación debe indicar la falta de evidencia.

Responde ÚNICAMENTE en JSON estricto sin markdown:
{{
  "situacion": "{situacion_usuario}",
  "principio_recomendado": "Nombre o 'N/A'",
  "explicacion": "Explicación breve",
  "recomendacion": "Recomendación o aviso de falta de evidencia",
  "evidencia": "Cita o 'N/A'",
  "encontrado_en_documento": true
}}
"""

response = client.responses.create(
    model=MODELO,
    input=[{"role": "user", "content": [{"type": "input_file", "file_id": file_id, "detail": "low"}, {"type": "input_text", "text": prompt}]}]
)

texto_limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.output_text.strip(), flags=re.MULTILINE)
datos = json.loads(texto_limpio)

with open(os.path.join(CARPETA_SALIDA, "ejercicio4_situacion.json"), "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("Ejercicio 4 completado exitosamente.")