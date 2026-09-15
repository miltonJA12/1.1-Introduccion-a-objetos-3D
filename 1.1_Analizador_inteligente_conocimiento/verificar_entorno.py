import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import openpyxl
import matplotlib

load_dotenv()

print("Python utilizado:", sys.executable)
print("OpenAI importado correctamente")
print("openpyxl importado correctamente")
print("matplotlib importado correctamente")

if os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY encontrada en el entorno")
else:
    print("ERROR: OPENAI_API_KEY no fue encontrada")

client = OpenAI()
print("Cliente de OpenAI creado correctamente")