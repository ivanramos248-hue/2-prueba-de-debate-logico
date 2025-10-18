from flask import Flask, render_template, request
import google.generativeai as genai
import os

# Configuración de Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    debate = ""
    if request.method == "POST":
        tema = request.form["tema"]

        modelo = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        Eres el moderador de un debate cósmico entre tres entidades de sabiduría universal:
        🌌 **Athena** — la razón y la lógica.
        🔥 **Prometheus** — la innovación y el cambio.
        💫 **Oráculo** — la intuición y la visión espiritual.

        Tema del debate: "{tema}"

        Cada entidad debe dar su perspectiva única.
        Luego, concluye con una síntesis armoniosa llamada
        **“Conclusión del Cosmos”**, donde integras los tres puntos de vista
        en una comprensión trascendente.

        Presenta el debate con estética literaria, fluida y poética,
        separando claramente las intervenciones.
        """

        respuesta = modelo.generate_content(prompt)
        debate = respuesta.text

    return render_template("index.html", debate=debate)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
