from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configura tu API key de Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/debate", methods=["POST"])
def debate():
    try:
        data = request.get_json()
        tema = data.get("tema", "")

        if not tema:
            return jsonify({"error": "Por favor ingresa un tema válido."}), 400

        # Usa el modelo correcto de Gemini
       modelo = genai.GenerativeModel("gemini-1.5-flash-latest")

        prompt = f"""
        Imagina un debate cósmico entre tres entidades del universo:
        🧠 Razón, 💫 Intuición y 🔥 Innovación.
        Tema del debate: {tema}.
        Cada entidad debe responder con una perspectiva breve, poética y única.
        """

        respuesta = modelo.generate_content(prompt)
        return jsonify({"resultado": respuesta.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
