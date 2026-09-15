import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path="../.env")

CARPETA_SALIDA = "."
RUTA_IDEAS = os.path.join("..", "ejercicio_1", "ejercicio1_ideas.json")
MAXIMO_EJEMPLOS = 1
MODELO = "gpt-4o-mini"
DOCUMENTO_PDF = "documento.pdf"

if not os.path.exists(RUTA_IDEAS):
    RUTA_IDEAS = os.path.join("ejercicio_1", "ejercicio1_ideas.json")

with open(RUTA_IDEAS, "r", encoding="utf-8") as f:
    lista_principios = json.load(f).get("ideas_principales", [])

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

prompt = f"""
Basándote en el PDF y en estos principios:
{json.dumps(lista_principios, ensure_ascii=False, indent=2)}

Localiza en el PDF hasta {MAXIMO_EJEMPLOS} ejemplo(s) por principio. Si no hay ejemplo claro, indícalo sin inventar.

Responde ÚNICAMENTE en JSON estricto sin markdown:
{{
  "ejemplos": [
    {{
      "principio_id": 1,
      "principio": "Nombre del principio",
      "contexto": "Contexto localizado",
      "situacion": "Situación descrita",
      "accion": "Acción realizada",
      "resultado": "Resultado obtenido",
      "relacion_con_principio": "Por qué lo respalda",
      "evidencia": "Cita breve"
    }}
  ]
}}
"""

response = client.responses.create(
    model=MODELO,
    input=[{"role": "user", "content": [{"type": "input_file", "file_id": file_id, "detail": "low"}, {"type": "input_text", "text": prompt}]}]
)

texto_limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.output_text.strip(), flags=re.MULTILINE)
datos = json.loads(texto_limpio)

with open(os.path.join(CARPETA_SALIDA, "ejercicio2_ejemplos.json"), "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("Ejercicio 2 completado exitosamente.")