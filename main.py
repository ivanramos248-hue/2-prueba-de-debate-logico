from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configura tu API Key de Gemini
genai.configure(api_key=os.environ.get("API_KEY_GEMINI"))

# Usa el modelo actualizado
modelo = genai.GenerativeModel("gemini-1.5-flash-latest")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/debate", methods=["POST"])
def debate():
    data = request.get_json()
    tema = data.get("tema", "")

    if not tema:
        return jsonify({"error": "Por favor ingresa un tema para debatir."}), 400

    prompt = f"""
    Inicia un debate lógico y creativo entre tres entidades del universo:
    - Razón
    - Intuición
    - Innovación

    Tema del debate: {tema}

    Presenta el intercambio como si fuera una conversación fluida, con ideas contrastantes.
    """

    try:
        respuesta = modelo.generate_content(prompt)
        return jsonify({"respuesta": respuesta.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
