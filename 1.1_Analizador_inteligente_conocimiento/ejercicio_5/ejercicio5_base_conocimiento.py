import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Cargar variables de entorno
load_dotenv(dotenv_path="../.env")

# 1. Definición de variables de entrada
CARPETA_SALIDA = "."  # Guarda directamente en ejercicio_5
MODELO = "gpt-4o-mini"
DOCUMENTO_PDF = "documento.pdf"

ARCHIVO_IDEAS_JSON = os.path.join("..", "ejercicio_1", "ejercicio1_ideas.json")
ARCHIVO_EJEMPLOS_JSON = os.path.join("..", "ejercicio_2", "ejercicio2_ejemplos.json")

# Verificar rutas si no se ejecuta desde la carpeta raíz
if not os.path.exists(ARCHIVO_IDEAS_JSON):
    ARCHIVO_IDEAS_JSON = os.path.join("ejercicio_1", "ejercicio1_ideas.json")
if not os.path.exists(ARCHIVO_EJEMPLOS_JSON):
    ARCHIVO_EJEMPLOS_JSON = os.path.join("ejercicio_2", "ejercicio2_ejemplos.json")

# Leer archivos JSON previos
with open(ARCHIVO_IDEAS_JSON, "r", encoding="utf-8") as f:
    datos_ideas = json.load(f)

with open(ARCHIVO_EJEMPLOS_JSON, "r", encoding="utf-8") as f:
    datos_ejemplos = json.load(f)

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
Basándote en el documento PDF y consolidando la información de los siguientes JSON previos:

- Ideas Principales (Ejercicio 1):
{json.dumps(datos_ideas, ensure_ascii=False, indent=2)}

- Ejemplos Prácticos (Ejercicio 2):
{json.dumps(datos_ejemplos, ensure_ascii=False, indent=2)}

Valida la relación entre ambos con el PDF y construye una Base de Conocimiento estructurada y completa.
Para cada principio integra el problema que resuelve y una aplicación práctica sugerida.

Debes responder ÚNICAMENTE en formato JSON estricto sin bloques de markdown con la siguiente estructura:
{{
  "base_conocimiento": [
    {{
      "id": 1,
      "principio": "Nombre del principio",
      "explicacion": "Explicación del principio",
      "problema_que_resuelve": "Conflicto o problema que ayuda a mitigar",
      "ejemplo": "Ejemplo ilustrativo proveniente del texto",
      "aplicacion_practica": "Cómo aplicar este principio en la vida cotidiana o laboral",
      "evidencia": "Cita o fragmento breve extraído del PDF"
    }}
  ]
}}
"""

# 3. Consulta a la API
print("Generando base de conocimiento integrada...")
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

texto_limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.output_text.strip(), flags=re.MULTILINE)
datos = json.loads(texto_limpio)

# Guardar JSON maestro
ruta_json_salida = os.path.join(CARPETA_SALIDA, "base_conocimiento.json")
with open(ruta_json_salida, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print(f"JSON maestro guardado en: {os.path.abspath(ruta_json_salida)}")

# 4. Exportar a Excel con openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Base de Conocimiento"

# Estilos visuales
font_cabecera = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
fill_cabecera = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
alineacion_centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
alineacion_izquierda = Alignment(horizontal="left", vertical="center", wrap_text=True)
borde_fino = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

encabezados = ["ID", "Principio", "Explicación", "Problema que Resuelve", "Ejemplo", "Aplicación Práctica", "Evidencia"]
ws.append(encabezados)

for col_num in range(1, len(encabezados) + 1):
    celda = ws.cell(row=1, column=col_num)
    celda.font = font_cabecera
    celda.fill = fill_cabecera
    celda.alignment = alineacion_centro

registros = datos.get("base_conocimiento", [])

for item in registros:
    ws.append([
        item.get("id"),
        item.get("principio"),
        item.get("explicacion"),
        item.get("problema_que_resuelve"),
        item.get("ejemplo"),
        item.get("aplicacion_practica"),
        item.get("evidencia")
    ])

for row in ws.iter_rows(min_row=2, max_row=len(registros) + 1):
    for cell in row:
        cell.border = borde_fino
        if cell.column == 1:
            cell.alignment = alineacion_centro
        else:
            cell.alignment = alineacion_izquierda

for col in ws.columns:
    col_letter = openpyxl.utils.get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = 25

ruta_excel_salida = os.path.join(CARPETA_SALIDA, "conocimiento_libro.xlsx")
wb.save(ruta_excel_salida)

print(f"Excel exportado con éxito en: {os.path.abspath(ruta_excel_salida)}")
print(f"Total de registros procesados: {len(registros)}")