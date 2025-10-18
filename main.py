# === MAIN DEBATE APP (versión corregida) ===
from flask import Flask, render_template, request, jsonify
from peca_engine.engine import iniciar_red_de_debate  # Importa el motor causal real
import google.generativeai as genai  # ✅ Librería correcta

# Configuración de la app Flask
app = Flask(__name__)

# Configura tu clave API (reemplaza aquí tu clave real)
genai.configure(api_key="AIzaSyCvAk9upRRvxNfQoeBbR_cs6Ffmm17DRvU")

# === RUTA PRINCIPAL ===
@app.route("/")
def index():
    return render_template("index.html")

# === RUTA PARA INICIAR EL DEBATE ===
@app.route("/iniciar_debate", methods=["POST"])
def iniciar_debate():
    try:
        pregunta = request.json.get("pregunta", "")
        if not pregunta:
            return jsonify({"error": "Debes ingresar una pregunta de debate."}), 400

        # Llamar al motor PECA para iniciar el debate entre las 3 IA
        conclusion, debates = iniciar_red_de_debate(pregunta)

        return jsonify({
            "pregunta": pregunta,
            "debates": debates,
            "conclusion_final": conclusion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === EJECUTAR LOCALMENTE ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
