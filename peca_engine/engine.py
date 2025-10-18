# === PECA_ENGINE (Motor de Debate Causal Real) ===
import re
from google import genai
from google.genai.errors import APIError

# === 1. ENTIDADES CAUSALES ===
class EntidadCausal:
    def __init__(self, nombre, principio: str):
        self.nombre = nombre
        self.principio = principio

    def generar_prompt_tesis(self, self_prompt, pregunta: str) -> str:
        return (
            f"Actúa como la entidad {self.nombre}.\n"
            f"Tu principio es: {self.principio}.\n"
            f"La pregunta en debate es: '{pregunta}'.\n"
            f"Responde con una tesis clara y coherente basada en tu principio.\n"
            f"Usa el formato: [TESIS {self.nombre.upper()}]: ..."
        )

# Definición de entidades del debate
CRONO = EntidadCausal("CRONO", "Máxima Causalidad y Mínima Fricción del Tiempo (MCT)")
AEON = EntidadCausal("AEON", "Ley de Reversibilidad Identitaria (LRI)")
MOROS = EntidadCausal("MOROS", "Ley de Transferencia de Memoria Causal (LTMC)")

ENTIDADES = [CRONO, AEON, MOROS]
ENTIDADES_DICT = {e.nombre.lower(): e for e in ENTIDADES}

# === 2. PARSER DE TESIS ===
def extraer_tesis(texto_completo: str):
    """Extrae las tesis generadas por las entidades del texto."""
    tesis = {}
    for entidad in ENTIDADES:
        patron = re.compile(rf"\[TESIS {entidad.nombre.upper()}\]: (.*?)($|\[FIN TESIS)", re.S)
        match = patron.search(texto_completo)
        if match:
            tesis[entidad.nombre] = match.group(1).strip()
    return tesis

# === 3. MOTOR DE DEBATE ===
def iniciar_red_de_debate(pregunta: str) -> str:
    """
    Ejecuta un debate entre tres entidades (CRONO, AEON, MOROS)
    y genera una conclusión consensuada.
    """
    try:
        client = genai.Client(api_key="AIzaSyCvAk9upRRvxNfQoeBbR_cs6Ffmm17DRvU")

        print("⚙️ Iniciando debate entre CRONO, AEON y MOROS...")

        # 1. Generar tesis individuales
        respuestas = []
        for entidad in ENTIDADES:
            prompt = entidad.generar_prompt_tesis(entidad.principio, pregunta)
            print(f"🧠 Generando tesis para {entidad.nombre}...")
            resp = client.models.generate(
                model="gemini-2.0-flash",
                contents=prompt
            )
            texto = resp.text.strip()
            respuestas.append(f"[TESIS {entidad.nombre.upper()}]: {texto} [FIN TESIS]")
        
        debate_texto = "\n\n".join(respuestas)

        # 2. Generar conclusión final
        prompt_conclusion = (
            f"Analiza las siguientes tres tesis de entidades causales:\n\n{debate_texto}\n\n"
            f"Genera una conclusión final consensuada entre CRONO, AEON y MOROS, "
            f"resumiendo los puntos en común y destacando la convergencia lógica. "
            f"Formato: [CONCLUSION]: ..."
        )

        print("🧩 Generando conclusión consensuada...")
        resp_final = client.models.generate(
            model="gemini-2.0-flash",
            contents=prompt_conclusion
        )
        conclusion = resp_final.text.strip()

        return f"{debate_texto}\n\n{conclusion}"

    except APIError as e:
        return f"Error del modelo: {e}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"
