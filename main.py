from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# RUTAS PRINCIPALES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debate')
def debate():
    return render_template('debate.html')

# NUEVA RUTA PARA RESPUESTAS
@app.route('/responder', methods=['POST'])
def responder():
    data = request.get_json()
    texto = data.get('texto', '').lower()

    # RESPUESTAS LÓGICAS SEGÚN EL CONTENIDO
    respuestas = {
        "CRONO": generar_respuesta("CRONO", texto),
        "AEON": generar_respuesta("AEON", texto),
        "MOROS": generar_respuesta("MOROS", texto)
    }

    return jsonify(respuestas)


# FUNCIÓN DE RESPUESTA POR CADA PERSONAJE
def generar_respuesta(personaje, texto):
    frases_generales = [
        "Interesante reflexión. Pero, ¿qué implica realmente eso en un contexto lógico?",
        "Esa afirmación merece ser cuestionada desde la base del razonamiento.",
        "¿Podrías justificar esa postura sin recurrir a una creencia previa?",
        "La lógica no siempre sigue al sentido común, sino a la consistencia interna.",
        "Cada afirmación necesita un fundamento. ¿Cuál sería el tuyo?"
    ]

    if "tiempo" in texto:
        if personaje == "CRONO":
            return "El tiempo es el marco invisible que condiciona toda deducción."
        elif personaje == "AEON":
            return "El tiempo es una ilusión de la mente que ordena lo inmutable."
        else:
            return "La razón trasciende el tiempo; sólo la percepción lo sufre."

    if "verdad" in texto:
        if personaje == "MOROS":
            return "La verdad es un peso que aplasta a quien no sabe sostenerla."
        elif personaje == "AEON":
            return "Toda verdad depende del orden lógico que la sustenta."
        else:
            return "El tiempo revela la verdad cuando todo error se agota."

    if "razón" in texto or "pensamiento" in texto:
        return random.choice([
            f"{personaje}: La razón debe guiarse por la coherencia antes que por la emoción.",
            f"{personaje}: El pensamiento crítico nace del conflicto entre ideas opuestas.",
            f"{personaje}: Razonar es depurar la mente del ruido emocional."
        ])

    return random.choice(frases_generales)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
