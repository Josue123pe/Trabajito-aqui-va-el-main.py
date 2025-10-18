from http.server import SimpleHTTPRequestHandler, HTTPServer

# Configura la dirección y el puerto
host = "localhost"
port = 8000

# Inicia un servidor HTTP simple
server = HTTPServer((host, port), SimpleHTTPRequestHandler)
print(f"Servidor corriendo en http://{host}:{port}")
print("Presiona Ctrl + C para detenerlo")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServidor detenido.")
    server.server_close()
