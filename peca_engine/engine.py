# === PECA_ENGINE (Motor de Debate Causal Real) ===
# === PECA_ENGINE (Motor de Debate Causal Real) ===
import re
import google.generativeai as genai
import os

# Configurar la API de Gemini desde las variables de entorno (Render + Environment)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# === 1. ENTIDADES CAUSALES ===
class EntidadCausal:
    def __init__(self, self_id, nombre, principio):
        self.id = self_id
        self.nombre = nombre
        self.principio = principio

    def generar_prompt(self, pregunta, contexto=""):
        """Genera la tesis inicial de la entidad basada en su principio."""
        return (
            f"Soy {self.nombre}. Mi principio rector es: '{self.principio}'. "
            f"Debato sobre: '{pregunta}'. "
            f"{contexto} "
            "Ofreceré un razonamiento breve y lógico que respalde mi postura.\n"
        )


# === 2. CONFIGURAR ENTIDADES ===
CRONO = EntidadCausal("CRONO", "CRONO", "Máxima Causalidad y Mínima Fricción del Tiempo (MCT)")
AEON = EntidadCausal("AEON", "AEON", "Ley de Reversibilidad Identitaria (LRI)")
MOROS = EntidadCausal("MOROS", "MOROS", "Ley de Transferencia de Memoria Causal (LTMC)")

ENTIDADES = [CRONO, AEON, MOROS]


# === 3. FUNCIONES AUXILIARES ===
def generar_respuesta(entidad, cliente, pregunta, contexto=""):
    """Llama a la API de Gemini para generar una respuesta de la entidad."""
    prompt = entidad.generar_prompt(pregunta, contexto)
    try:
        response = cliente.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except APIError as e:
        return f"[Error con {entidad.nombre}: {e}]"


def construir_dialogo(pregunta, respuestas_previas):
    """Crea un resumen de las respuestas anteriores para contextualizar la conversación."""
    contexto = "Resumen del debate hasta ahora:\n"
    for entidad, respuesta in respuestas_previas.items():
        contexto += f"{entidad}: {respuesta}\n"
    contexto += "\nResponde con base en este contexto y añade tu razonamiento.\n"
    return contexto


# === 4. FUNCIÓN PRINCIPAL ===
def iniciar_red_de_debate(pregunta):
    """Ejecuta el ciclo completo del debate causal entre las tres entidades."""
    cliente = genai.Client(api_key="AIZAisyCvAk9URpRWuQfoQBeBR_cS6fFmmt7DRVU")  # 👈 Tu API Key

    debate = {}
    contexto = ""

    # Paso 1: cada entidad da su postura inicial
    for entidad in ENTIDADES:
        debate[entidad.nombre] = generar_respuesta(entidad, cliente, pregunta, contexto)
        contexto = construir_dialogo(pregunta, debate)

    # Paso 2: generación de conclusión final consensuada
    prompt_final = (
        "Tres inteligencias (CRONO, AEON y MOROS) han debatido sobre una pregunta. "
        "A continuación se resumen sus respuestas:\n\n"
        f"{contexto}\n"
        "Ahora, como moderador neutral, sintetiza sus ideas en una conclusión final "
        "que refleje los puntos de coincidencia más profundos y lógicos entre las tres posturas."
    )

    try:
        conclusion = cliente.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt_final
        )
        conclusion_texto = conclusion.text.strip()
    except APIError as e:
        conclusion_texto = f"[Error al generar la conclusión: {e}]"

    # Paso 3: devolver el resultado completo
    resultado = {
        "pregunta": pregunta,
        "respuestas": debate,
        "conclusion": conclusion_texto
    }
    return resultado

