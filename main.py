from flask import Flask, render_template, request
import google.generativeai as genai
import os

# Configuración de la API de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    debate = None
    error = None

    if request.method == "POST":
        tema = request.form.get("tema")

        try:
            # Modelo actualizado
            modelo = genai.GenerativeModel("gemini-1.5-flash-latest")

            # Prompt del debate cósmico
            prompt = f"""
            Eres el moderador de un debate cósmico entre tres entidades de sabiduría universal:
            🌙 **Athena** = la razón y la lógica.
            🔥 **Prometheus** = la innovación y el cambio.
            🔮 **Oráculo** = la intuición y la visión espiritual.

            Tema del debate: "{tema}"

            Cada entidad debe dar su perspectiva única.
            Luego, concluye con una síntesis armoniosa llamada:
            ✨ "Conclusión del Cosmos" ✨ que integra los tres puntos de vista
            en una comprensión trascendente.

            El texto debe estar bien estructurado, con nombres claros antes de cada intervención,
            y en formato narrativo atractivo.
            """

            respuesta = modelo.generate_content(prompt)
            debate = respuesta.text

        except Exception as e:
            error = f"Ocurrió un error: {str(e)}"

    return render_template("index.html", debate=debate, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
