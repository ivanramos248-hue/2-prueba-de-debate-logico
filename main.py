
from flask import Flask, render_template, request
import google.generativeai as genai
import os

# === 1. Configuración de la API de Google ===
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# === 2. Clase para generar tesis ===
class EntidadCausal:
    def __init__(self, nombre, principio):
        self.nombre = nombre
        self.principio = principio

    def generar_tesis(self, pregunta):
        prompt = (
            f"Actúa como la entidad {self.nombre}, guiada por el principio '{self.principio}'. "
            f"Responde a la siguiente pregunta de forma lógica, concisa y filosófica.\n\n"
            f"Pregunta: {pregunta}"
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        respuesta = model.generate_content(prompt)
        return respuesta.text.strip()

# === 3. Crear entidades ===
CRONO = EntidadCausal("CRONO", "tiempo y consecuencia")
AEON = EntidadCausal("AEON", "equilibrio y permanencia")
MOROS = EntidadCausal("MOROS", "inevitabilidad y destino")

# === 4. Configurar Flask ===
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/debatir", methods=["POST"])
def debatir():
    pregunta = request.form["pregunta"]

    t_crono = CRONO.generar_tesis(pregunta)
    t_aeon = AEON.generar_tesis(pregunta)
    t_moros = MOROS.generar_tesis(pregunta)

    return render_template(
        "resultado.html",
        pregunta=pregunta,
        crono=t_crono,
        aeon=t_aeon,
        moros=t_moros
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
