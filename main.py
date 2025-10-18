from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Ruta principal (pantalla de bienvenida)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar la plantilla del debate
@app.route('/debate')
def debate():
    return render_template('debate.html')

# Ruta para simular el debate entre las IAs
@app.route('/iniciar', methods=['POST'])
def iniciar_debate():
    cronos = [
        "El tiempo es un recurso que determina la lógica de nuestras decisiones.",
        "Toda acción humana está sujeta al orden temporal del pensamiento.",
        "Reflexionemos sobre cómo el tiempo influye en la razón."
    ]
    aeon = [
        "El razonamiento trasciende el tiempo cuando buscamos la verdad absoluta.",
        "El conocimiento no depende de la secuencia, sino de la conexión entre ideas.",
        "El pensamiento lógico es atemporal, aunque se exprese en el presente."
    ]
    moros = [
        "La consecuencia de no razonar lógicamente es el caos argumentativo.",
        "Sin estructura lógica, el diálogo se convierte en ruido.",
        "Toda verdad carece de sentido sin el peso de la deducción correcta."
    ]

    debate = [
        {"orador": "CRONO", "texto": random.choice(cronos)},
        {"orador": "AEON", "texto": random.choice(aeon)},
        {"orador": "MOROS", "texto": random.choice(moros)}
    ]

    return jsonify(debate)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
