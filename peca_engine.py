# === PECA_ENGINE (Motor de Debate Causal Real) ===
import re
from google import genai
from google.genai.errors import APIError

# === 1. ENTIDADES CAUSALES ===
class EntidadCausal:
    def __init__(self, nombre: str, principio: str):
        self.nombre = nombre
        self.principio = principio

    def generar_prompt_tesis(self, pregunta: str) -> str:
        return (f"Actúa como la entidad '{self.nombre}'. "
                f"Tu principio es: {self.principio}. "
                f"La pregunta es: '{pregunta}'. "
                f"Genera una tesis breve con formato exacto: "
                f"[TESIS {self.nombre.upper()}] ... [FIN TESIS {self.nombre.upper()}].")

CRONO = EntidadCausal("CRONO", "Máxima Causalidad y Mínima Fricción (LDI)")
AEON = EntidadCausal("AEON", "Ley de Reversibilidad Entrópica (LRE)")
MOROS = EntidadCausal("MOROS", "Ley de Transferencia de Memoria Causal (LTMC)")

ENTIDADES = [CRONO, AEON, MOROS]
ENTIDADES_DICT = {e.nombre: e for e in ENTIDADES}

# === 2. PARSER ROBUSTO ===
def extraer_tesis(texto_completo: str):
    tesis = {}
    for entidad in ENTIDADES:
        patron = re.compile(rf"\[TESIS {entidad.nombre.upper()}\](.*?)(?:\[FIN TESIS {entidad.nombre.upper()}\]|$)", re.DOTALL)
        match = patron.search(texto_completo)
        if match:
            tesis[entidad.nombre] = match.group(1).strip()
    return tesis

# === 3. MOTOR PRINCIPAL ===
def iniciar_red_de_debate(pregunta_causal: str, api_key: str):
    try:
        client = genai.Client(api_key=api_key)
        model = "gemini-2.0-flash"

        print("\n🔷 Iniciando PECA Engine")
        print(f"🔸 Pregunta causal: {pregunta_causal}\n")

        respuestas_raw = {}
        for entidad in ENTIDADES:
            prompt = entidad.generar_prompt_tesis(pregunta_causal)
            response = client.models.generate_content(model=model, contents=prompt)
            respuestas_raw[entidad.nombre] = response.text
            print(f"✅ {entidad.nombre} generó su tesis.")

        debate_input = "\n".join(respuestas_raw.values())
        tesis_extraidas = extraer_tesis(debate_input)

        if len(tesis_extraidas) != len(ENTIDADES):
            print("⚠️ Error: faltan tesis o etiquetas incorrectas.")
            return

        prompt_final = f"Eres el motor de CONVERGENCIA CAUSAL. Pregunta: '{pregunta_causal}'. "
        for n, t in tesis_extraidas.items():
            prompt_final += f"\n- {n}: {t}"
        prompt_final += "\nUne los argumentos en una conclusión lógica y final."

        response_final = client.models.generate_content(model=model, contents=prompt_final)
        print("\n🚀 CONVERGENCIA CAUSAL FINAL:")
        print(response_final.text)

    except APIError as e:
        print(f"❌ Error API: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")
