from flask import Flask, render_template, request
import google.generativeai as genai
import os

# Configuración de Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    debate = ""
    error_message = ""  # <-- Nueva variable para mostrar errores

    if request.method == "POST":
        try:
            tema = request.form["tema"]

            # Carga del modelo actualizado
            modelo = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
            Eres el moderador de un debate cósmico entre tres entidades de sabiduría universal:
            🌙 **Athena** – la razón y la lógica.
            🔥 **Prometheus** – la innovación y el cambio.
            🔮 **Oráculo** – la intuición y la visión espiritual.

            Tema del debate: “{tema}”

            Cada entidad debe dar su perspectiva única.
            Luego, concluye con una síntesis armoniosa llamada
            **Conclusión del Cosmos**, donde integras los tres puntos de vista
            en una comprensión trascendente.
            """

            respuesta = modelo.generate_content(prompt)
            debate = respuesta.text

        except Exception as e:
            # Captura errores (como claves incorrectas o fallos del modelo)
            error_message = f"Ocurrió un error: {str(e)}"

    return render_template("index.html", debate=debate, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
