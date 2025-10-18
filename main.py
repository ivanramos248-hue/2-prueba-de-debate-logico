# main.py — app Flask para la app Debate Lógico (versión final)
import os
from flask import Flask, render_template, request, jsonify

# Importa la función pública del motor PECA que ya implementaste
# Debe aceptar (pregunta: str, api_key: str) y devolver un resultado (texto o dict).
from peca_engine.engine import iniciar_red_de_debate

app = Flask(__name__)

# Leemos la clave desde la variable de entorno (Render > Environment)
API_KEY = os.getenv("GEMINI_API_KEY")

# RUTA PRINCIPAL: página de bienvenida (usa templates/index.html)
@app.route("/")
def index():
    return render_template("index.html")

# RUTA DE LA PÁGINA DE DEBATE (muestra interfaz con botón Iniciar)
@app.route("/debate")
def debate_page():
    return render_template("debate.html")

# API: iniciar debate. Recibe JSON: { "pregunta": "texto..." }
@app.route("/api/start_debate", methods=["POST"])
def api_start_debate():
    data = request.get_json(silent=True) or {}
    pregunta = data.get("pregunta", "").strip()
    if not pregunta:
        return jsonify({"error": "Debes enviar 'pregunta' en el body JSON."}), 400

    # Seguridad: no poner la clave en el código; la toma el engine desde el parámetro o entorno
    if not API_KEY:
        return jsonify({"error": "API key no configurada en el servidor (GEMINI_API_KEY)."}), 500

    try:
        # Llama al motor real. Se espera que devuelva texto o dict.
        resultado = iniciar_red_de_debate(pregunta_causal=pregunta, api_key=API_KEY)

        # Si tu engine imprime y no devuelve, capturamos ese caso:
        if resultado is None:
            return jsonify({"message": "El motor ejecutó el debate. Revisa los logs del servidor para ver la salida."}), 200

        # Respuesta normal: devolvemos lo que retorne el engine
        return jsonify({"pregunta": pregunta, "resultado": resultado}), 200

    except Exception as e:
        # Devuelve error útil para debugging (en producción ocultar mensaje completo)
        return jsonify({"error": "Error ejecutando el motor PECA.", "detail": str(e)}), 500


# Endpoint sanity / healthcheck
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Para desarrollo local:
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
