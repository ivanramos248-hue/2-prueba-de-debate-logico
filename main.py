# === main.py ===
from flask import Flask, render_template, request, jsonify
from peca_engine.engine import iniciar_red_de_debate

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/debate", methods=["POST"])
def debate():
    data = request.get_json()
    pregunta = data.get("pregunta", "").strip()

    if not pregunta:
        return jsonify({"error": "⚠️ Ingresa un tema para debatir."}), 400

    try:
        resultado = iniciar_red_de_debate(pregunta)
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"error": f"❌ Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
