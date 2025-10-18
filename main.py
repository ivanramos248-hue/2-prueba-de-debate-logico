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
            f"Actúa como la entidad ({self.nombre}), guiada por el principio ({self.principio}). "
            f"Responde de forma clara y lógica a la siguiente pregunta:\n\n"
            f"Pregunta: {pregunta}"
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        respuesta = model.generate_content(prompt)
        return respuesta.text.strip()

# === 3. Crear entidades ===
CRONO = EntidadCausal("CRONO", "tiempo y consecuencia")
AEON = EntidadCausal("AEON", "equilibrio y permanencia")
MOROS = EntidadCausal("MOROS", "inevitabilidad y destino")

# === 4. Función de debate lógico ===
def debate_logico(pregunta):
    return {
        "pregunta": pregunta,
        "CRONO": CRONO.generar_tesis(pregunta),
        "AEON": AEON.generar_tesis(pregunta),
        "MOROS": MOROS.generar_tesis(pregunta)
    }

# === 5. Servidor Flask ===
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        pregunta = request.form["pregunta"]
        resultado = debate_logico(pregunta)
        return render_template("index.html", resultado=resultado)
    return render_template("index.html", resultado=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

