from flask import Flask, request, send_file, render_template_string, url_for
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

@app.route("/descargar", methods=["GET"])
def descargar():
    if not os.path.exists(RUTA_ARCHIVO):
        return "Aún no hay registros."
    return send_file(RUTA_ARCHIVO, as_attachment=True)

@app.route("/ver", methods=["GET"])
def ver():
    if not os.path.exists(RUTA_ARCHIVO):
        return "Aún no hay registros."
    with open(RUTA_ARCHIVO, encoding="utf-8") as f:
        reader = csv.reader(f)
        filas = list(reader)
    tabla_html = """
    <html><head><title>Registros</title></head><body>
    <h2>Registros de Acceso</h2>
    <a href="{}" download><button>📥 Descargar CSV</button></a><br><br>
    <table border="1" cellpadding="6" cellspacing="0">
    <tr>{}</tr>
    {}
    </table></body></html>
    """.format(
        url_for('descargar'),
        ''.join(f'<th>{col}</th>' for col in filas[0]),
        ''.join('<tr>' + ''.join(f'<td>{dato}</td>' for dato in fila) + '</tr>' for fila in filas[1:])
    )
    return render_template_string(tabla_html)

@app.route("/")
def home():
    return "Backend de registro operativo."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
