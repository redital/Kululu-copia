from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import os
import base64
from datetime import datetime
from config import Config, flask_app_config

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la cartella se non esiste

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # Se il caricamento avviene tramite file (immagini o video)
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            return redirect(url_for('index'))

    # Se il caricamento avviene tramite webcam (solo foto in base64)
    data = request.json.get("image")
    if data:
        image_data = base64.b64decode(data.split(",")[1])
        filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_data)

        return jsonify({"message": "Foto salvata!", "filename": filename})

    return jsonify({"error": "Nessun file ricevuto"}), 400

@app.route("/media")
def get_media():
    """ Restituisce l'elenco dei file salvati (immagini e video) """
    files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    files = ordina_foto(files)[::-1]
    return jsonify(files)

def date_parser(nome_foto):
    stringa_data = nome_foto[6:-4]
    data = datetime.strptime(stringa_data, '%Y%m%d_%H%M%S')
    return data

def ordina_foto(lista_foto):
    dizionario_date = {i: date_parser(i) for i in lista_foto}
    sort_dates = lambda x: dict(sorted(x.items(), key=lambda item: item[1]))
    dizionario_date = sort_dates(dizionario_date)
    return list(dizionario_date.keys())

@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(**flask_app_config)
