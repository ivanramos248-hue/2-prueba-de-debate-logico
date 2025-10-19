from flask import Flask, send_from_directory, render_template

app = Flask(__name__)

# Ruta principal que sirve el index.html desde /static
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Ruta para el debate (si existe)
@app.route('/debate')
def debate():
    return render_template('debate.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
