import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde el archivo .env en la raíz
load_dotenv(dotenv_path="../.env")

# ==========================================
# 1. DEFINICIÓN DE VARIABLES DE ENTRADA
# ==========================================
CARPETA_SALIDA = "."  # Guarda directamente en la carpeta actual (ejercicio_7)
MODELO = "gpt-4o-mini"
DOCUMENTO_PDF = "documento.pdf"

# Variables para personalizar la evaluación
cantidad_preguntas = 5
dificultad = "intermedio"  # Opciones: fácil, intermedio, difícil
tipo_pregunta = "opción múltiple"
tema = "principios de relaciones humanas y liderazgo"

# Inicializar cliente de OpenAI
client = OpenAI()
path_pdf = DOCUMENTO_PDF if os.path.exists(DOCUMENTO_PDF) else os.path.join("..", DOCUMENTO_PDF)

# Función para reutilizar el file_id guardado en file_id.txt (evita resubir el PDF)
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

# Obtener el file_id
file_id = obtener_file_id(client, path_pdf)

# ==========================================
# 2. CONSTRUCCIÓN DEL PROMPT Y SOLICITUD API
# ==========================================
prompt = f"""
Basándote ÚNICAMENTE en el contenido del documento PDF adjunto, genera un banco de preguntas con las siguientes especificaciones:
- Cantidad de preguntas: {cantidad_preguntas}
- Dificultad: {dificultad}
- Tipo de pregunta: {tipo_pregunta}
- Tema/Sección: {tema}

Cada pregunta debe contar con exactamente 4 opciones de respuesta (A, B, C, D), indicar cuál es la respuesta correcta, la explicación detallada, el principio relacionado y la evidencia textual extraída del PDF.

Debes responder ÚNICAMENTE en formato JSON estricto sin bloques de markdown con la siguiente estructura:
{{
  "preguntas": [
    {{
      "pregunta_id": 1,
      "pregunta": "Texto de la pregunta",
      "opciones": [
        {{"opcion": "A", "texto": "Opción A"}},
        {{"opcion": "B", "texto": "Opción B"}},
        {{"opcion": "C", "texto": "Opción C"}},
        {{"opcion": "D", "texto": "Opción D"}}
      ],
      "respuesta_correcta": "A",
      "explicacion": "Explicación según el PDF",
      "principio_relacionado": "Nombre del principio",
      "evidencia": "Cita o fragmento breve del PDF"
    }}
  ]
}}
"""

print("Enviando petición a la Responses API de OpenAI...")
# Se envía la lista de entradas donde se combina la referencia al PDF (file_id) y el prompt de usuario
response = client.responses.create(
    model=MODELO,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_file", "file_id": file_id, "detail": "low"}, # Referencia al PDF subido
                {"type": "input_text", "text": prompt}                       # Instrucciones y variables
            ]
        }
    ]
)

# Capturar el texto de salida recibido de la API
output_text = response.output_text

# Limpiar posibles bloques markdown ```json ... ```
texto_limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", output_text.strip(), flags=re.MULTILINE)

# ==========================================
# 3. PROCESAMIENTO Y GUARDADO
# ==========================================
try:
    # Convertir el string JSON recibido a un diccionario Python
    datos = json.loads(texto_limpio)
    
    # Guardar en ejercicio7_preguntas.json
    ruta_json_salida = os.path.join(CARPETA_SALIDA, "ejercicio7_preguntas.json")
    with open(ruta_json_salida, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        
    print(f"\n¡Éxito! Banco de preguntas guardado en: {os.path.abspath(ruta_json_salida)}\n")

    # ==========================================
    # 4. EVALUACIÓN INTERACTIVA EN TERMINAL
    # ==========================================
    print("==================================================")
    print("      INICIO DE LA EVALUACIÓN INTERACTIVA")
    print("==================================================\n")
    
    preguntas = datos.get("preguntas", [])
    aciertos = 0

    for idx, preg in enumerate(preguntas, 1):
        print(f"Pregunta {idx} de {len(preguntas)}: {preg['pregunta']}")
        for opt in preg["opciones"]:
            print(f"  {opt['opcion']}) {opt['texto']}")
        
        # Pedir respuesta al usuario
        respuesta_usuario = input("\nTu respuesta (A, B, C, D): ").strip().upper()
        
        # Comparación con la respuesta correcta
        if respuesta_usuario == preg["respuesta_correcta"]:
            print(" ¡CORRECTO!")
            aciertos += 1
        else:
            print(f" INCORRECTO. La respuesta correcta era: {preg['respuesta_correcta']}")
        
        print(f"Explicación: {preg['explicacion']}")
        print(f"Principio: {preg['principio_relacionado']}")
        print("-" * 50 + "\n")

    print(f"RESULTADO FINAL: {aciertos} aciertos de {len(preguntas)} preguntas ({int((aciertos/len(preguntas))*100)}%).\n")

except json.JSONDecodeError as e:
    print("Error al decodificar la respuesta JSON:", e)