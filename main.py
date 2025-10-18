from flask import Flask, render_template, request, jsonify
import random
from peca_engine.engine import iniciar_red_de_debate  # 👈 Importa el motor causal real

app = Flask(__name__)

# === RUTAS PRINCIPALES ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate')
def debate():
    return render_template('debate.html')

# === RUTA NUEVA: genera el debate real ===
@app.route('/responder', methods=['POST'])
def responder():
    data = request.get_json()
    pregunta = data.get('texto', '').strip()

    if not pregunta:
        return jsonify({"error": "No se recibió ninguna pregunta."}), 400

    # Llamar al motor causal real
    resultado = iniciar_red_de_debate(pregunta)

    return jsonify({"respuesta": resultado})


# === INICIO DEL SERVIDOR ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
