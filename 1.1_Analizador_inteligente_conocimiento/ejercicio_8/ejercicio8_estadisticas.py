import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import matplotlib.pyplot as plt

# Cargar variables de entorno desde el .env en la raíz
load_dotenv(dotenv_path="../.env")

# 1. Definición de variables de entrada
CARPETA_SALIDA = "."  # Guarda directamente dentro de la carpeta ejercicio_8
MODELO = "gpt-4o-mini"
DOCUMENTO_PDF = "documento.pdf"

# Categorías para la clasificación semántica
CATEGORIAS = [
    "Liderazgo",
    "Comunicación",
    "Persuasión",
    "Gestión de Conflictos",
    "Desarrollo Personal"
]

RUTA_IDEAS_JSON = os.path.join("..", "ejercicio_1", "ejercicio1_ideas.json")
if not os.path.exists(RUTA_IDEAS_JSON):
    RUTA_IDEAS_JSON = os.path.join("ejercicio_1", "ejercicio1_ideas.json")

# Leer las ideas extraídas en el Ejercicio 1
with open(RUTA_IDEAS_JSON, "r", encoding="utf-8") as f:
    datos_ideas = json.load(f)

ideas_json = datos_ideas.get("ideas_principales", [])

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

# 2. Construcción del Prompt para Clasificación Semántica (IA)
prompt = f"""
Analiza las siguientes ideas extraídas del PDF:
{json.dumps(ideas_json, ensure_ascii=False, indent=2)}

Clasifica cada idea ÚNICAMENTE en una de las siguientes categorías:
{json.dumps(CATEGORIAS, ensure_ascii=False, indent=2)}

Debes responder ÚNICAMENTE en formato JSON estricto sin bloques de markdown con la siguiente estructura:
{{
  "clasificacion_estadistica": [
    {{
      "idea_id": 1,
      "categoria": "Nombre de la categoría seleccionada",
      "justificacion": "Explicación breve de la clasificación según el PDF"
    }}
  ]
}}
"""

print("Solicitando clasificación semántica a la API...")
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
datos_api = json.loads(texto_limpio)

# ==========================================
# 3. PROCESAMIENTO ESTADÍSTICO TRADICIONAL (PYTHON)
# ==========================================
clasificaciones = datos_api.get("clasificacion_estadistica", [])
total_ideas = len(clasificaciones)

# Contar frecuencias con un algoritmo en Python
conteo_frecuencias = {cat: 0 for cat in CATEGORIAS}
for item in clasificaciones:
    cat = item.get("categoria")
    if cat in conteo_frecuencias:
        conteo_frecuencias[cat] += 1
    else:
        conteo_frecuencias[cat] = 1

# Calcular porcentajes
estadisticas = []
print("\n=== TABLA DE FRECUENCIAS Y PORCENTAJES ===")
print(f"{'Categoría':<25} | {'Frecuencia':<10} | {'Porcentaje':<10}")
print("-" * 52)

for cat, freq in conteo_frecuencias.items():
    pct = (freq / total_ideas * 100) if total_ideas > 0 else 0
    estadisticas.append({
        "categoria": cat,
        "frecuencia": freq,
        "porcentaje": round(pct, 2)
    })
    print(f"{cat:<25} | {freq:<10} | {pct:.1f}%")

# Guardar los datos combinados en ejercicio8_estadisticas.json
resultado_final = {
    "clasificacion_individual": clasificaciones,
    "resumen_estadistico": estadisticas,
    "total_ideas_analizadas": total_ideas
}

ruta_json_salida = os.path.join(CARPETA_SALIDA, "ejercicio8_estadisticas.json")
with open(ruta_json_salida, "w", encoding="utf-8") as f:
    json.dump(resultado_final, f, ensure_ascii=False, indent=2)

print(f"\nDatos guardados en: {os.path.abspath(ruta_json_salida)}")

# ==========================================
# 4. GENERACIÓN DE GRÁFICA CON MATPLOTLIB
# ==========================================
categorias_nombres = [item["categoria"] for item in estadisticas]
frecuencias_valores = [item["frecuencia"] for item in estadisticas]

plt.figure(figsize=(9, 5))
barras = plt.bar(categorias_nombres, frecuencias_valores, color='#2b5c8f', edgecolor='black')

plt.title('Distribución de Ideas Principales por Categoría', fontsize=12, fontweight='bold')
plt.xlabel('Categorías', fontsize=10)
plt.ylabel('Cantidad de Ideas (Frecuencia)', fontsize=10)
plt.ylim(0, max(frecuencias_valores) + 2 if frecuencias_valores else 5)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Añadir las etiquetas numéricas sobre cada barra
for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2.0, yval + 0.1, int(yval), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()

ruta_grafica = os.path.join(CARPETA_SALIDA, "ejercicio8_estadisticas.png")
plt.savefig(ruta_grafica, dpi=300)
plt.close()

print(f"Gráfica guardada en: {os.path.abspath(ruta_grafica)}")