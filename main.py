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

# --- Inicializar Pusher solo una vez ---
pusher_client = pusher.Pusher(
    app_id='2065491',
    key='08f9ca3827443d276de3',
    secret='63d6cd6ed91c56e3521d',
    cluster='mt1',
    ssl=True
)

# --- Ruta principal: recibe y reenvía mensaje ---
@app.route("/", methods=["POST"])
def recibir_mensaje():
    data = request.get_json() or {}

    # Obtener datos
    message = data.get("message", "")
    canal = data.get("canal", "my-channel")  # Canal por defecto si no se envía

    if not message:
        return jsonify({"error": "Mensaje vacío"}), 400

    # Guardar en base de datos
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mensajes (mensaje, canal) VALUES (%s, %s)", (message, canal))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error al guardar en base de datos:", e)
        return jsonify({"error": "No se pudo guardar el mensaje"}), 500

    # Enviar al canal correspondiente
    try:
        pusher_client.trigger(canal, 'my-event', {"message": message})
    except Exception as e:
        print("❌ Error al enviar mensaje a Pusher:", e)
        return jsonify({"error": "Error al enviar a Pusher"}), 500

    return jsonify({"status": "ok", "canal": canal, "mensaje": message})


# --- Ruta para listar mensajes ---
@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, mensaje, canal, fecha FROM mensajes ORDER BY fecha DESC")
        mensajes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(mensajes)
    except Exception as e:
        print("❌ Error al obtener mensajes:", e)
        return jsonify({"error": "No se pudieron obtener los mensajes"}), 500


if __name__ == "__main__":
    app.run(debug=True)
