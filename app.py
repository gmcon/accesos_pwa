from flask import Flask, request, render_template_string, url_for
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

SHEETDB_API_URL = "https://sheetdb.io/api/v1/cf7nxftgn1pil"

@app.route("/registro", methods=["POST"])
def registrar():
    try:
        datos = request.get_json(force=True)
        print("📦 Datos recibidos:", datos)
    except Exception as e:
        print("❌ Error al obtener JSON:", e)
        return {"estado": "error", "mensaje": "Error al interpretar JSON"}, 400

    alumno_id = datos.get("id")
    fecha = datos.get("fecha", datetime.utcnow().isoformat())

    if not alumno_id:
        return {"estado": "error", "mensaje": "Falta ID"}, 400

    payload = {"data": {"alumno_id": alumno_id, "fecha": fecha}}
    try:
        response = requests.post(SHEETDB_API_URL, json=payload)
        print(f"✔ Intento de registro: {alumno_id} a las {fecha}")
        print(f"📡 Código respuesta: {response.status_code}")
        print(f"📄 Respuesta texto: {response.text}")

    except Exception as e:
        print("❌ Error al enviar a SheetDB:", e)
        return {"estado": "error", "mensaje": "No se pudo registrar en SheetDB"}, 500

    return {"estado": "ok"}, 200

@app.route("/ver")
def ver():
    return f"Puedes revisar los registros en tu hoja de cálculo aquí: <a href='https://docs.google.com/spreadsheets/d/'>Abrir hoja</a>"

@app.route("/")
def home():
    return "Backend de registro operativo conectado a Google Sheets vía SheetDB."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
