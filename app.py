from flask import Flask, request
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

RUTA_ARCHIVO = "registros.csv"

@app.route("/registro", methods=["POST"])
def registrar():
    print("🛰 request.data crudo:", request.data)
    print("📨 request.headers:", dict(request.headers))
    try:
        datos = request.get_json(force=True)
        print("📦 Datos forzados recibidos:", datos)
    except Exception as e:
        print("❌ Error al obtener JSON:", e)
        return {"estado": "error", "mensaje": "Error al interpretar JSON"}, 400

    alumno_id = datos.get("id")
    fecha = datos.get("fecha", datetime.utcnow().isoformat())

    if not alumno_id:
        return {"estado": "error", "mensaje": "Falta ID"}, 400

    nuevo = [alumno_id, fecha]

    archivo_existe = os.path.exists(RUTA_ARCHIVO)
    with open(RUTA_ARCHIVO, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(["alumno_id", "fecha"])
        writer.writerow(nuevo)

    print(f"✔ Registro recibido: {alumno_id} a las {fecha}")
    return {"estado": "ok"}, 200

@app.route("/")
def home():
    return "Backend de registro operativo."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
