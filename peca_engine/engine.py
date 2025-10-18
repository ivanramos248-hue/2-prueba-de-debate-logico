# === peca_engine/engine.py ===
# Motor PECA (Pensamiento y Explicación Causal Artificial)
# Versión final compatible con Gemini (GenerativeModel)

import os
import re
import google.generativeai as genai

# === CONFIGURACIÓN GEMINI ===
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise EnvironmentError("⚠️ La variable GEMINI_API_KEY no está definida en el entorno.")

# Configura Gemini con la API key del entorno
genai.configure(api_key=API_KEY)

# Modelo que usaremos
MODEL_NAME = "gemini-2.0-flash"

# Función utilitaria para generar texto desde un prompt
def generar_respuesta(prompt):
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()

# === ENTIDADES CAUSALES ===
class EntidadCausal:
    def __init__(self, id_name, nombre, principio):
        self.id = id_name
        self.nombre = nombre
        self.principio = principio

    def generar_prompt_tesis(self, pregunta):
        return (
            f"Soy {self.nombre}. Mi principio rector es: {self.principio}.\n"
            f"Debato sobre: {pregunta}.\n"
            "Ofreceré un razonamiento lógico que respalde mi postura.\n"
        )

# === CONFIGURAR LAS TRES ENTIDADES ===
CRONO = EntidadCausal("crono", "CRONO", "Máxima Causalidad y Mínima Fricción del Tiempo (MCT)")
AEON = EntidadCausal("aeon", "AEON", "Ley de Reversibilidad Entrópica (LRE)")
MOROS = EntidadCausal("moros", "MOROS", "Ley de Transferencia de Memoria Causal (LTMC)")

ENTIDADES = [CRONO, AEON, MOROS]

# === FUNCIÓN PRINCIPAL: Iniciar debate ===
def iniciar_red_de_debate(pregunta_causal, api_key=None):
    """
    Ejecuta un debate lógico entre las 3 entidades usando el modelo Gemini.
    Devuelve un resumen final.
    """
    print(f"\n🧠 Iniciando debate lógico sobre: '{pregunta_causal}'\n")

    resultados = []

    for entidad in ENTIDADES:
        prompt = entidad.generar_prompt_tesis(pregunta_causal)
        try:
            print(f"💬 {entidad.nombre} está generando su argumento...")
            respuesta = generar_respuesta(prompt)
            resultados.append((entidad.nombre, respuesta))
        except Exception as e:
            resultados.append((entidad.nombre, f"⚠️ Error: {e}"))

    # Crear conclusión final combinando todas las posturas
    resumen_prompt = (
        "A continuación se muestran tres argumentos causales sobre un mismo tema.\n"
        "Tu tarea es analizarlos y crear una conclusión equilibrada, clara y reflexiva.\n\n"
    )
    for nombre, texto in resultados:
        resumen_prompt += f"{nombre} dice:\n{texto}\n\n"

    resumen_prompt += "Genera una conclusión final integradora del debate."

    print("\n🧩 Generando conclusión final...")
    conclusion = generar_respuesta(resumen_prompt)

    # Devolver todo como texto estructurado
    resultado_texto = "🧠 DEBATE FINAL\n\n"
    for nombre, texto in resultados:
        resultado_texto += f"=== {nombre} ===\n{texto}\n\n"
    resultado_texto += f"💡 CONCLUSIÓN FINAL:\n{conclusion}\n"

    print("✅ Debate completado.\n")
    return resultado_texto
