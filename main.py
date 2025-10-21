from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import pusher

app = Flask(__name__)
CORS(app)

# 🔒 Datos de conexión a MySQL (puedes moverlos a variables de entorno también)
DB_CONFIG = {
    "host": "mysql-rodriguez.alwaysdata.net",
    "user": "rodriguez",
    "password": "latesitorr",
    "database": "rodriguez_tareasisi"
}

# 🔑 Configuración de Pusher (idealmente usar variables de entorno)
pusher_client = pusher.Pusher(
    app_id="2065491",
    key="08f9ca3827443d276de3",
    secret="63d6cd6ed91c56e3521d",
    cluster="mt1",
    ssl=True
)

@app.route("/", methods=["POST"])
def recibir_mensaje():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Mensaje vacío"}), 400

    try:
        # 1️⃣ Guardar mensaje en MySQL
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mensajes (mensaje) VALUES (%s)", (message,))
        conn.commit()
        cursor.close()
        conn.close()

        # 2️⃣ Enviar mensaje a Pusher
        pusher_client.trigger("my-channel", "my-event", {"message": message})

        return jsonify({"status": "ok", "message": message}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    """Permite obtener los mensajes guardados (por si luego quieres mostrarlos)."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mensajes ORDER BY fecha DESC")
        mensajes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(mensajes), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
