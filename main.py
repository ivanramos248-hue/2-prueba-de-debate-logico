from flask import Flask, render_template, request, jsonify
import os
from peca_engine.engine import iniciar_red_de_debate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/debate")
def debate():
    return render_template("debate.html")

@app.route("/api/iniciar_debate", methods=["POST"])
def api_iniciar_debate():
    data = request.get_json()
    pregunta = data.get("pregunta", "").strip()
    if not pregunta:
        return jsonify({"error": "Debes escribir una pregunta."}), 400
    try:
        result = iniciar_red_de_debate(pregunta)
        return jsonify({"ok": True, "resultado": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
