# peca_engine/engine.py
import os
import re
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise EnvironmentError("La variable GEMINI_API_KEY no está definida en el entorno.")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

class EntidadCausal:
    def __init__(self, id_name, nombre, principio):
        self.id = id_name
        self.nombre = nombre
        self.principio = principio

    def generar_prompt_tesis(self, pregunta):
        return (
            f"Actúa como la entidad '{self.nombre}' cuyo principio es '{self.principio}'.\n"
            f"Genera una tesis breve sobre: \"{pregunta}\".\n"
            f"Usa el formato exacto: [TESIS {self.nombre.upper()}] ... [FIN TESIS {self.nombre.upper()}]."
        )

CRONO = EntidadCausal("crono", "CRONO", "Máxima Causalidad y Mínima Fricción")
AEON  = EntidadCausal("aeon",  "AEON",  "Ley de Reversibilidad Entrópica (LRE)")
MOROS = EntidadCausal("moros", "MOROS", "Ley de Transferencia de Memoria Causal (LTMC)")

ENTIDADES = [CRONO, AEON, MOROS]

def extraer_tesis(texto):
    resultados = {}
    for ent in ENTIDADES:
        patron = re.compile(rf"\[TESIS {ent.nombre.upper()}\](.*?)\[FIN TESIS {ent.nombre.upper()}\]", re.S)
        m = patron.search(texto)
        if m:
            resultados[ent.nombre] = m.group(1).strip()
    return resultados

def generar_contenido(prompt):
    resp = client.models.generate_content(model=MODEL, contents=prompt)
    return getattr(resp, "text", str(resp)).strip()

def iniciar_red_de_debate(pregunta):
    if not pregunta:
        raise ValueError("Debes escribir una pregunta.")
    
    # 1. Generar tesis individuales
    raw_tesis = {}
    for ent in ENTIDADES:
        prompt = ent.generar_prompt_tesis(pregunta)
        raw_tesis[ent.nombre] = generar_contenido(prompt)
    
    ensamblado = "\n".join(raw_tesis.values())
    tesis = extraer_tesis(ensamblado)
    for ent in ENTIDADES:
        if ent.nombre not in tesis:
            tesis[ent.nombre] = raw_tesis[ent.nombre]
    
    # 2. Pedir convergencia final
    prompt_final = (
        f"Estas son las tesis sobre '{pregunta}'. Refútalas y unifica las ideas.\n\n"
        f"{ensamblado}\n\n"
        f"Escribe al final: 🚀 CONVERGENCIA CAUSAL (PECA) FINAL: <conclusión>"
    )
    conclusion = generar_contenido(prompt_final)
    
    return {"pregunta": pregunta, "tesis_parsed": tesis, "conclusion_raw": conclusion, "raw_tesis": raw_tesis}
