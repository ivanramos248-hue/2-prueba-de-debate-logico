# === main.py ===
from flask import Flask, render_template, request
from peca_engine.engine import iniciar_red_de_debate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    debate_result = ""
    pregunta = ""

    if request.method == "POST":
        pregunta = request.form["pregunta"]
        if pregunta.strip():
            debate_result = iniciar_red_de_debate(pregunta)

    return render_template("index.html", debate_result=debate_result, pregunta=pregunta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
