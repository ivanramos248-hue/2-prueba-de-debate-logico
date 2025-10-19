from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configurar la API key desde variables de entorno
genai.configure(api_key=os.getenv("API_KEY_GEMINI"))

# Crear el modelo Gemini
modelo = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/debate", methods=["POST"])
def debate():
    try:
        data = request.get_json()
        tema = data.get("tema", "")
        if not tema:
            return jsonify({"error": "Tema no proporcionado"}), 400

        prompt = f"Organiza un debate entre Razón, Intuición e Innovación sobre: {tema}"
        respuesta = modelo.generate_content(prompt)
        return jsonify({"respuesta": respuesta.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
