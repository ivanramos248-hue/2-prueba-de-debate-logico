from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    # Renderiza el index.html desde /static
    return send_from_directory('static', 'index.html')

@app.route('/debate', methods=['GET', 'POST'])
def debate():
    respuesta = None
    if request.method == 'POST':
        argumento = request.form.get('argumento')
        # Aquí puedes agregar tu lógica del "motor del debate"
        respuesta = f"Interesante punto: {argumento}"
    return render_template('debate.html', respuesta=respuesta)

@app.route('/ping')
def ping():
    return "Pong! ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
