import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde el .env de la raíz
load_dotenv(dotenv_path="../.env")

# 1. Definición de variables de entrada
CARPETA_SALIDA = "."  # Guarda directamente dentro de ejercicio_6
MODELO = "gpt-4o-mini"
DOCUMENTO_PDF = "documento.pdf"

# Categorías permitidas (Límite estricto para la IA)
CATEGORIAS_PERMITIDAS = [
    "Liderazgo y Gestión de Equipos",
    "Resolución de Conflictos",
    "Comunicación y Persuasión",
    "Relaciones Interpersonales",
    "Desarrollo Personal"
]

# Lista de 10 situaciones para clasificar
SITUACIONES = [
    "Un empleado se niega a colaborar con un nuevo proyecto porque siente que no tomaron en cuenta sus ideas.",
    "Dos compañeros de trabajo discuten acaloradamente en medio de la oficina sobre de quién fue la culpa de un retraso.",
    "Un cliente llama muy enfadado exigiendo la devolución de su dinero por un servicio que no cumplió sus expectativas.",
    "Un líder necesita dar retroalimentación a un colaborador cuyo rendimiento ha bajado significativamente este mes.",
    "Un gerente quiere convencer a su equipo de adoptar un nuevo software sin generar resistencia al cambio.",
    "Un miembro del equipo llega constantemente tarde a las reuniones diarias interrumpiendo el flujo de trabajo.",
    "Un profesional siente frustración porque sus colegas no lo escuchan durante las sesiones de lluvia de ideas.",
    "Un supervisor cometió un error en un informe financiero y no sabe cómo comunicárselo a su superior.",
    "Un vendedor intenta cerrar un trato con un cliente difícil que siempre pone objeciones al precio.",
    "Un empleado recibe un reconocimiento público pero su compañero directo se muestra resentido por ello."
]

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

# 2. Construcción del Prompt
prompt = f"""
Basándote ÚNICAMENTE en el documento PDF adjunto, analiza y clasifica la siguiente lista de situaciones:

Situaciones:
{json.dumps(SITUACIONES, ensure_ascii=False, indent=2)}

Categorías permitidas:
{json.dumps(CATEGORIAS_PERMITIDAS, ensure_ascii=False, indent=2)}

Reglas estrictas:
1. Asigna a cada situación ÚNICAMENTE una categoría de la lista 'categorias_permitidas'. No inventes nuevas categorías.
2. Identifica un principio recomendado presente en el PDF. No inventes principios ausentes en el documento.
3. Proporciona una justificación y la evidencia (cita breve) correspondiente.

Debes responder ÚNICAMENTE en formato JSON estricto sin bloques de markdown con la siguiente estructura:
{{
  "clasificaciones": [
    {{
      "id": 1,
      "situacion": "Texto de la situación",
      "categoria": "Categoría seleccionada de la lista permitida",
      "principio_recomendado": "Principio encontrado en el PDF",
      "justificacion": "Explicación de por qué este principio y categoría aplican",
      "evidencia": "Cita o fragmento breve extraído del PDF"
    }}
  ]
}}
"""

# 3. Llamada a la Responses API
print("Procesando clasificación de 10 situaciones con OpenAI...")
response = client.responses.create(
    model=MODELO,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_file", "file_id": file_id, "detail": "low"},
                {"type": "input_text", "text": prompt}
            ]
        }
    ]
)

output_text = response.output_text

# Limpiar formato Markdown en caso de incluir ```json ... ```
texto_limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", output_text.strip(), flags=re.MULTILINE)

# 4. Guardar archivo de salida
try:
    datos = json.loads(texto_limpio)
    ruta_json_salida = os.path.join(CARPETA_SALIDA, "ejercicio6_clasificacion.json")
    
    with open(ruta_json_salida, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        
    print(f"\n¡Éxito! Clasificación guardada en: {os.path.abspath(ruta_json_salida)}")
    print(f"Total de situaciones clasificadas: {len(datos.get('clasificaciones', []))}\n")
    
    for item in datos.get("clasificaciones", [])[:3]:
        print(f"[{item['id']}] Categoría: {item['categoria']}")
        print(f"    Situación: {item['situacion'][:60]}...")
        print(f"    Principio: {item['principio_recomendado']}\n")

except json.JSONDecodeError as e:
    print("Error al decodificar la respuesta JSON:", e)