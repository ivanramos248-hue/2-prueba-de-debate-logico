# === peca_engine/engine.py ===
import os
import google.generativeai as genai

# Obtener la API key desde Render
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise EnvironmentError("⚠️ La variable GEMINI_API_KEY no está definida en el entorno.")

# Configurar cliente Gemini
genai.configure(api_key=API_KEY)
MODEL = "gemini-1.5-pro-latest"

# === CLASES ===
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

# === FUNCIÓN PRINCIPAL ===
def iniciar_red_de_debate(pregunta):
    """
    Genera la conversación de debate entre las tres entidades usando Gemini.
    """
    debate_prompt = f"""
    Imagina un debate filosófico entre tres entidades lógicas:
    - {CRONO.nombre}: representa la {CRONO.principio}.
    - {AEON.nombre}: representa la {AEON.principio}.
    - {MOROS.nombre}: representa la {MOROS.principio}.

    Tema del debate: "{pregunta}"

    Cada entidad debe argumentar desde su principio lógico.
    Finaliza con una breve conclusión integradora.
    """

    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(debate_prompt)

        if response and response.text:
            return response.text
        else:
            return "⚠️ No se recibió respuesta del modelo."

    except Exception as e:
        return f"❌ Error interno: {str(e)}"
