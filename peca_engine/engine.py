# === peca_engine/engine.py ===
import os
import google.generativeai as genai

# Obtener la API key desde Render
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise EnvironmentError("⚠️ La variable GEMINI_API_KEY no está definida en el entorno.")

# Configurar cliente Gemini
genai.configure(api_key=API_KEY)
MODEL = "gemini-1.5-flash"

# --- CLASES ---
class EntidadCausal:
    def __init__(self, id_name, nombre, principio):
        self.id = id_name
        self.nombre = nombre
        self.principio = principio

    def generar_tesis(self, pregunta):
        return f"Soy {self.nombre}, basado en mi principio '{self.principio}', pienso que: {pregunta}"

# Entidades principales
CRONO = EntidadCausal("crono", "CRONO", "Máxima Causalidad y Mínima Fricción")
AEON = EntidadCausal("aeon", "AEON", "Ley de Reversibilidad Entrópica (LRE)")
MOROS = EntidadCausal("moros", "MOROS", "Ley de Transferencia de Memoria Causal (LTMC)")

# --- FUNCIÓN PRINCIPAL ---
def iniciar_red_de_debate(pregunta):
    """
    Lógica completa del debate y la conclusión generada por Gemini.
    """
    debate_prompt = f"""
    Tres entidades — CRONO, AEON y MOROS — están debatiendo sobre la siguiente pregunta:
    "{pregunta}"

    Cada una debe presentar su postura basada en su principio.
    Luego, generen un intercambio corto entre ellas y terminen con una CONCLUSIÓN FINAL UNIFICADA.

    Principios:
    - CRONO: Máxima Causalidad y Mínima Fricción
    - AEON: Ley de Reversibilidad Entrópica (LRE)
    - MOROS: Ley de Transferencia de Memoria Causal (LTMC)

    Formato de salida:
    🌀 [Inicio del Debate]
    💬 CRONO: ...
    💬 AEON: ...
    💬 MOROS: ...
    🔄 Interacción entre ellos (máximo 3 turnos)
    🧠 Conclusión Final: ...
    """

    model = genai.GenerativeModel(MODEL)
    respuesta = model.generate_content(debate_prompt)
    return respuesta.text
