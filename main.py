from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configurar la API Key de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Crear el modelo
modelo = genai.GenerativeModel("gemini-pro")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/debate", methods=["POST"])
def debate():
    try:
        data = request.get_json()
        tema = data.get("tema", "debate cósmico")

        prompt = f"""
        Imagina un debate cósmico entre tres entidades: Razón, Intuición e Innovación.
        Tema del debate: "{tema}"
        Escribe un diálogo breve y equilibrado entre ellas, donde cada una exprese su perspectiva única.
        """

        respuesta = modelo.generate_content(prompt)
        texto = respuesta.text.strip() if respuesta and respuesta.text else "No se pudo generar el debate."

        return jsonify({"resultado": texto})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
