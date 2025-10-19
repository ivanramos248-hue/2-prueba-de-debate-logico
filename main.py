from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Página principal (sirve index.html desde /static)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Página del debate (usa templates/debate.html)
@app.route('/debate')
def debate():
    return render_template('debate.html')

# Prueba básica
@app.route('/ping')
def ping():
    return "Servidor activo 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
