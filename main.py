from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import pusher

app = Flask(__name__)
CORS(app)

# --- Configuración de base de datos ---
db_config = {
    "host": "mysql-rodriguez.alwaysdata.net",
    "user": "rodriguez",
    "password": "latesitorr",
    "database": "rodriguez_tareasisi"
}

# --- Ruta principal: recibe mensaje ---
@app.route("/", methods=["POST"])
def recibir_mensaje():
    data = request.get_json()

    # Inicializar Pusher
    pusher_client = pusher.Pusher(
        app_id='2065491',
        key='08f9ca3827443d276de3',
        secret='63d6cd6ed91c56e3521d',
        cluster='mt1',
        ssl=True
    )

    # Obtener mensaje del JSON recibido
    message = data.get("message", "") if data else ""

    # Guardar en la base de datos
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mensajes (mensaje) VALUES (%s)", (message,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error al guardar en base de datos:", e)

    # Enviar a Pusher
    pusher_client.trigger('my-channel', 'my-event', message)
    return jsonify({"status": "ok", "mensaje": message})


# --- Nueva ruta: listar mensajes ---
@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, mensaje, fecha FROM mensajes ORDER BY fecha DESC")
        mensajes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(mensajes)
    except Exception as e:
        print("❌ Error al obtener mensajes:", e)
        return jsonify({"error": "No se pudieron obtener los mensajes"}), 500


if __name__ == "__main__":
    app.run(debug=True)
