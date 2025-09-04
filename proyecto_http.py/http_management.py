"""
http_management.py
Manejo de solicitudes HTTP (POST) para recibir logs de clientes,
validar token, y guardarlos en la base de datos.
"""

# -----------------------------
# Importamos librerías
# -----------------------------
from http.server import BaseHTTPRequestHandler  # Para manejar cada request HTTP
import json                                      # Para manejar datos en formato JSON
from http_db_connect import cargar_log_a_db      # Función que guarda logs en la DB
from tokens import VALID_TOKENS                  # Diccionario con tokens válidos

"""
http_management.py
Manejo de solicitudes HTTP para recibir logs (POST) y consultar logs (GET) de clientes.
Todo explicado paso a paso.
"""

# -----------------------------
# Importamos librerías
# -----------------------------
from http.server import BaseHTTPRequestHandler        # Clase base para manejar requests HTTP
import json                                          # Para convertir entre dict y JSON
from http_db_connect import cargar_log_a_db          # Función que guarda logs en la DB
from tokens import VALID_TOKENS                      # Diccionario con tokens válidos
from urllib.parse import urlparse, parse_qs          # Para parsear query params en GET

# -----------------------------
# Creamos nuestra clase de manejo de requests
# -----------------------------
class LogRequestHandler(BaseHTTPRequestHandler):

    # -----------------------------
    # Función que maneja los POST requests
    # -----------------------------
    def do_POST(self):
        # 1) Verificar que la ruta sea /logs
        if self.path != "/logs":
            self.send_response(404)  # Ruta no existe
            self.end_headers()
            self.wfile.write(("Endpoint no encontrado").encode("utf-8"))  # Siempre enviamos bytes
            return

        # -----------------------------
        # 2) Validar token en headers
        # -----------------------------
        auth_header = self.headers.get("Authorization", "")  # Tomamos el header "Authorization"

        # Revisamos que empiece con "Token "
        if not auth_header.startswith("Token "):
            self.send_response(401)  # No autorizado
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Quién sos, bro?"}).encode("utf-8"))
            return

        # Extraemos el token del header
        token = auth_header.split(" ")[1]

        # Revisamos si el token está en nuestra lista de tokens válidos
        if token not in VALID_TOKENS:
            self.send_response(403)  # Prohibido
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Quién sos, bro?"}).encode("utf-8"))
            return

        # -----------------------------
        # 3) Leer el body (JSON enviado por cliente)
        # -----------------------------
        content_length = int(self.headers.get("Content-Length", 0))  # Tamaño del body
        body = self.rfile.read(content_length)                        # Leemos los bytes del body
        body_str = body.decode("utf-8")                               # Convertimos bytes a string

        # -----------------------------
        # 4) Guardar en la base de datos
        # -----------------------------
        try:
            # Usamos el cursor y la conexión que asignamos al server en http_server.py
            # self.server.cursor -> cursor de la DB
            # self.server.db_conn -> conexión a la DB
            cargar_log_a_db(self.server.cursor, self.server.db_conn, body_str)

            # Respondemos OK al cliente
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "log recibido correctamente"}).encode("utf-8"))

        except Exception as e:
            # Si hay cualquier error, enviamos error 500 al cliente
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    # -----------------------------
    # Función que maneja los GET requests
    # -----------------------------
    def do_GET(self):
        # 1) Solo permitimos /logs
        if not self.path.startswith("/logs"):
            self.send_response(404)  # Ruta no existe
            self.end_headers()
            self.wfile.write("Endpoint no encontrado".encode("utf-8"))
            return

        # -----------------------------
        # 2) Parsear parámetros de la URL
        # Ejemplo: /logs?timestamp_start=2025-09-01T00:00:00Z&timestamp_end=2025-09-03T23:59:59Z
        # -----------------------------
        url = urlparse(self.path)           # Separa ruta y query
        params = parse_qs(url.query)        # Convierte query string en diccionario

        timestamp_start = params.get("timestamp_start", [None])[0]
        timestamp_end = params.get("timestamp_end", [None])[0]
        received_start = params.get("received_at_start", [None])[0]
        received_end = params.get("received_at_end", [None])[0]

        # -----------------------------
        # 3) Construir la consulta SQL dinámicamente
        # -----------------------------
        query = "SELECT * FROM eventos_logs WHERE 1=1"  # 1=1 nos permite agregar AND fácilmente
        args = []

        if timestamp_start:
            query += " AND timestamps >= ?"
            args.append(timestamp_start)
        if timestamp_end:
            query += " AND timestamps <= ?"
            args.append(timestamp_end)
        if received_start:
            query += " AND received_at >= ?"
            args.append(received_start)
        if received_end:
            query += " AND received_at <= ?"
            args.append(received_end)

        # -----------------------------
        # 4) Ejecutar la consulta en la DB
        # -----------------------------
        cursor = self.server.cursor           # Obtenemos cursor de la DB
        cursor.execute(query, args)           # Ejecutamos consulta con parámetros
        resultados = cursor.fetchall()        # Traemos todos los resultados

        # -----------------------------
        # 5) Formatear los resultados como lista de diccionarios
        # -----------------------------
        logs = []
        for row in resultados:
            logs.append({
                "id": row[0],
                "autor": row[1],
                "timestamp": row[2],
                "service": row[3],
                "severity": row[4],
                "message": row[5],
                "received_at": row[6]
            })

        # -----------------------------
        # 6) Enviar la respuesta al cliente en JSON
        # -----------------------------
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(logs, indent=2).encode("utf-8"))
