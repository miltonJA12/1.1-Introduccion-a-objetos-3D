import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde el .env en la raíz
load_dotenv(dotenv_path="../.env")

# 1. Definición de variables de entrada
CARPETA_SALIDA = "."  # Guarda dentro de ejercicio_9
MODELO = "gpt-4o-mini"
DOCUMENTO_PDF = "documento.pdf"

client = OpenAI()
path_pdf = DOCUMENTO_PDF if os.path.exists(DOCUMENTO_PDF) else os.path.join("..", DOCUMENTO_PDF)

# Función de reutilización de file_id
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

# Entrada interactiva
pregunta_usuario = input("\nEscribe la pregunta a verificar: ").strip()

# 2. Construcción del prompt_control
prompt_control = f"""
Pregunta del usuario: "{pregunta_usuario}"

REGLAS DE CONTROL DE VERIFICACIÓN ESTRUCTURAL:
1. Responde EXCLUSIVAMENTE utilizando información explícita contenida en el PDF adjunto. NO utilices conocimiento externo ni asumas datos.
2. Si la información solicitada se encuentra en el documento:
   - "encontrado_en_documento" debe ser true.
   - "respuesta" debe ser la explicación extraída del texto.
   - "evidencia" debe incluir la cita o fragmento del PDF.
   - "explicacion_verificacion" debe señalar la ubicación o contexto textual.
3. Si no hay evidencia suficiente o la pregunta es ajena al documento:
   - "encontrado_en_documento" debe ser false.
   - "respuesta" debe ser EXACTAMENTE el texto: "INFORMACIÓN NO ENCONTRADA EN EL DOCUMENTO".
   - "evidencia" debe ser un string vacío "".
   - "explicacion_verificacion" debe explicar que no se localizó evidencia suficiente.

Debes responder ÚNICAMENTE en formato JSON estricto sin bloques de markdown con la siguiente estructura:
{{
  "encontrado_en_documento": true,
  "respuesta": "string",
  "evidencia": "string",
  "explicacion_verificacion": "string"
}}
"""

# 3. Llamada a la Responses API
print("Verificando si la respuesta existe en el documento PDF...")
response = client.responses.create(
    model=MODELO,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_file", "file_id": file_id, "detail": "low"},
                {"type": "input_text", "text": prompt_control}
            ]
        }
    ]
)

output_text = response.output_text
texto_limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", output_text.strip(), flags=re.MULTILINE)

# 4. Procesamiento y guardado acumulativo
try:
    datos_respuesta = json.loads(texto_limpio)
    ruta_json = os.path.join(CARPETA_SALIDA, "ejercicio9_verificacion.json")
    
    # Leer el historial existente si ya hay consultas previas guardadas
    historial = []
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                historial = json.load(f)
                if not isinstance(historial, list):
                    historial = [historial]
        except json.JSONDecodeError:
            historial = []
            
    # Agregar la nueva entrada con la pregunta hecha
    registro = {
        "pregunta": pregunta_usuario,
        "resultado": datos_respuesta
    }
    historial.append(registro)
    
    # Guardar en ejercicio9_verificacion.json
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)
        
    print(f"\n¡Éxito! Consulta guardada en: {os.path.abspath(ruta_json)}")
    print("\n--- RESULTADO DE VERIFICACIÓN ---")
    print(f"¿Encontrado?: {datos_respuesta.get('encontrado_en_documento')}")
    print(f"Respuesta: {datos_respuesta.get('respuesta')}")
    print(f"Evidencia: {datos_respuesta.get('evidencia')}")
    print(f"Explicación: {datos_respuesta.get('explicacion_verificacion')}\n")

except json.JSONDecodeError as e:
    print("Error al decodificar la respuesta JSON:", e)