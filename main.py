# main.py

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import traceback
import sys
# Importa el SDK de Gemini
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# OpenAI se deshabilita para enfocarnos en Gemini
openai = None 

app = Flask(__name__, static_folder="static", template_folder="templates")

# -------------------------------------------------------
# Helper: generar texto usando Gemini
# -------------------------------------------------------
def generar_con_gemini(prompt: str):
    if genai is None:
        raise RuntimeError("google-generativeai no instalado. Instale: pip install google-generativeai")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY no encontrada. Asegúrate de configurarla.")
    
    genai.configure(api_key=api_key)
    
    # Modelos: Intentamos gemini-1.5-flash (el más capaz) y luego gemini-pro (el estándar)
    # 1024 tokens asegura espacio para el debate completo.
    MAX_TOKENS = 1024
    
    # Lista de modelos ajustada: 1.5-flash y luego pro
    for model_name in ("gemini-1.5-flash", "gemini-pro"): 
        try:
            # Crea el cliente del modelo
            model = genai.GenerativeModel(model_name=model_name)
            
            # Genera el contenido con la configuración de tokens
            resp = model.generate_content(
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    max_output_tokens=MAX_TOKENS
                )
            )
            
            # Devuelve el texto generado
            return resp.text
        
        except Exception as e:
            # Captura y registra el error para el siguiente intento
            sys.stderr.write(f"Error con modelo {model_name}: {e}\n")
            continue
            
    # Si todos los modelos fallan
    raise RuntimeError("No se pudo generar con Gemini: todos los modelos intentados fallaron o clave sin permisos.")

# -------------------------------------------------------
# Endpointes
# -------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return send_from_directory("static", "index.html")

@app.route("/debate", methods=["GET", "POST"])
def debate_page():
    # Detecta si la petición es un formulario tradicional o AJAX
    tema = None
    is_json = request.is_json
    
    if is_json and request.json:
        tema = request.json.get("tema")
    elif request.form:
        tema = request.form.get("argumento")

    if request.method == "GET":
        return render_template("debate.html")
    
    if not tema:
        # Respuesta de error adaptada al tipo de solicitud
        if is_json:
            return jsonify({"error": "Por favor escribe un tema."}), 400
        else:
            return render_template("debate.html", respuesta="Por favor escribe un tema."), 400

    # prepara prompt que exige 3 voces + conclusión
    prompt = f"""
    Moderador: organiza un debate entre tres entidades: RAZÓN, INTUICIÓN e INNOVACIÓN.
    Tema: {tema}

    Requerimientos:
    - Cada entidad debe dar una tesis corta (1-2 frases).
    - Luego debe responder brevemente a las otras entidades (1 frase).
    - Finalmente, escribe una "Conclusión Unificada" (3-4 frases) que integre los puntos.
    Formato: etiqueta cada intervención con [RAZON], [INTUICION], [INNOVACION] y termina con [CONCLUSION].
    """

    # Intenta Gemini -> Demo
    last_error = None
    resultado = None
    
    try:
        # 1. Intentar con Gemini
        if os.getenv("GEMINI_API_KEY") and genai is not None:
            resultado = generar_con_gemini(prompt)
            # Si tiene éxito, devuelve el resultado
            return render_template("debate.html", respuesta=resultado)
    except Exception as e:
        last_error = f"ERROR GEMINI: {e}"
        # Continuar al modo demo si falla

    # 2. Modo demo: respuesta simulada si no hay clave o si falló la API
    demo = (
        "[RAZON]\nLa mejor estrategia es analizar datos y priorizar eficiencia.\n\n"
        "[INTUICION]\nSiento que la adaptabilidad y el contexto humano son clave.\n\n"
        "[INNOVACION]\nPropondría un experimento rápido para validar las ideas.\n\n"
        "[CONCLUSION]\nIntegrando razonamiento, intuición e innovación, lo óptimo es iterar rápidamente con métricas claras."
    )
    
    # Si hubo errores, los añadimos para el desarrollador
    if last_error:
        demo += f"\n\n--- MODO DEMO | Error de conexión (revisa tu clave): {last_error}"
    
    return render_template("debate.html", respuesta=demo)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Servidor activo"})

# run
if __name__ == "__main__":
    # Usa un puerto por defecto (10000) o el definido por el entorno (Render)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
