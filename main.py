# === PECA: Sistema de Debate Lógico entre Entidades Causales ===
# Versión lista para Render.com
# Autor: Iván Ramos + Asistente GPT-5

from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# === 1. Configuración de la API ===
# Reemplaza el texto entre comillas con tu API Key de Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "TU_API_KEY_AQUI")
genai.configure(api_key=GEMINI_API_KEY)

# === 2. Definición de entidades ===
class EntidadCausal:
    def __init__(self, nombre, principio):
        self.nombre = nombre
        self.principio = principio

    def generar_tesis(self, pregunta):
        prompt = (
            f"Actúa como la entidad {self.nombre}, guiada por el principio {self.principio}. "
            f"Responde a la pregunta de forma clara y lógica.\n\n"
            f"Pregunta: {pregunta}"
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        respuesta = model.generate_content(prompt)
        return respuesta.text.strip()

# === 3. Crear entidades ===
CRONO = EntidadCausal("CRONO", "tiempo y consecuencia")
AEON = EntidadCausal("AEON", "equilibrio y permanencia")
MOROS = EntidadCausal("MOROS", "inevitabilidad y destino")

# === 4. Debate lógico ===
def debate_logico(pregunta):
    t_crono = CRONO.generar_tesis(pregunta)
    t_aeon = AEON.generar_tesis(pregunta)
    t_moros = MOROS.generar_tesis(pregunta)

    return {
        "pregunta": pregunta,
        "CRONO": t_crono,
        "AEON": t_aeon,
        "MOROS": t_moros
    }

# === 5. Servidor Flask para Render ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 PECA: Sistema de Debate Lógico entre humanos e IA"
