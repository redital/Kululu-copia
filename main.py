from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
from datetime import datetime
from config import Config, flask_app_config

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la cartella se non esiste

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json.get("image")  # Otteniamo l'immagine in base64
    if not data:
        return jsonify({"error": "Nessuna immagine ricevuta"}), 400
    
    # Decodifica l'immagine
    image_data = base64.b64decode(data.split(",")[1])
    filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, "wb") as f:
        f.write(image_data)

    return jsonify({"message": "Foto salvata!", "filename": filename})

@app.route("/images")
def get_images():
    """ Restituisce l'elenco delle immagini salvate """
    images = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".png")]
    return jsonify(images)

@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(**flask_app_config)
