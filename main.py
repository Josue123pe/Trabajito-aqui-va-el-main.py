from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/", methods=[ "POST"])
def hola_mundo():
    import pusher
    data = request.get_json()
   
    pusher_client = pusher.Pusher(
        app_id = '2065491',
        key = "08f9ca3827443d276de3",
        secret = "63d6cd6ed91c56e3521d",
        cluster = "mt1",
        ssl=True
    )

    if data and "message" in data:
        message = data["message"]
    else:
        message = request.form.get("message") or request.get_data(as_text=True) or ""

    pusher_client.trigger('my-channel', 'my-event', message)
    return ".."

if __name__ == "__main__":
    app.run(debug=True)