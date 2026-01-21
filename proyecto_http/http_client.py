"""
http_client.py
Cliente HTTP que genera logs, los guarda localmente y los envía al servidor.
"""

# -----------------------------
# Importamos librerías
# -----------------------------
import time                         # Para hacer pausas entre envíos
import urllib.request               # Para enviar requests HTTP
import urllib.error                 # Para manejar errores HTTP

from http_db_connect import crear_conectar_db, crear_log, cargar_log_a_db    # Funciones de DB

# --------------------------------------------
# 1) Configuración de la base de datos local
# --------------------------------------------
# 1a) Creamos o conectamos a la DB local
lista_de_logs = crear_conectar_db()

# 1b) Creamos el cursor para ejecutar consultas
cursor = lista_de_logs.cursor()

# ------------------------------------
# 2) Configuración del servidor HTTP
# ------------------------------------
SERVER_URL = "http://localhost:8000/logs"   # Endpoint de logs del servidor
TOKEN = "TOKEN456"                          # Token válido para enviar logs

# --------------------------------
# 3) Bucle principal del cliente
# --------------------------------

numero_de_intentos = 3
numero_hechos = 0

while numero_hechos < numero_de_intentos:
    # 3a) Generamos un log de ejemplo
    # La función crear_log devuelve un string JSON listo para enviar o guardar
    mensaje_json = crear_log(
        autor="cliente1",
        service="send_text_service",
        severity="INFO",
        mensaje="Este es un log de prueba"
    )

    # 3b) Mostramos en consola el log generado
    print(f"Log generado y listo para enviar: {mensaje_json}")

    # 3c) Guardamos el log también en la DB local del cliente
    cargar_log_a_db(cursor, lista_de_logs, mensaje_json)

    # 3d) Enviamos el log al servidor HTTP
    try:
        # Convertimos el JSON a bytes para enviarlo en el body
        data = mensaje_json.encode("utf-8")

        # Creamos el request con el header Authorization
        request = urllib.request.Request(
            url=SERVER_URL,
            data=data,                       # Body con log en bytes
            headers={
                "Content-Type": "application/json",  # Indicamos que enviamos JSON
                "Authorization": f"Token {TOKEN}"   # Token para validar en el servidor
            },
            method="POST"
        )

        # Ejecutamos la request y leemos la respuesta del servidor
        with urllib.request.urlopen(request) as response:
            resp_body = response.read().decode("utf-8")
            print(f"Respuesta del servidor: {resp_body}")

    except urllib.error.HTTPError as e:
        # Error HTTP (por ejemplo 401, 403, 404, 500)
        print(f"[ERROR] HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        # No se pudo conectar al servidor
        print(f"[ERROR] No se pudo conectar al servidor: {e.reason}")
    except Exception as e:
        # Otro error inesperado
        print(f"[ERROR] Error inesperado: {e}")

    # 3e) Esperamos un ratito antes de generar el siguiente log
    time.sleep(5)
    numero_hechos += 1
    
    if numero_de_intentos == numero_hechos:
        break


# -----------
# Log Falso: 
# -----------

mensaje_json = crear_log(
        autor="cliente1",
        service="send_text_service",
        severity="INFO",
        mensaje="Este es un log falso de prueba"
    )

# Mostramos en consola el log falso generado
print(f"Log falso generado y listo para enviar: {mensaje_json}")

# Enviamos el log falso al servidor HTTP
try:
    # Convertimos el JSON a bytes para enviarlo en el body
    data = mensaje_json.encode("utf-8")

    # Creamos el request con el header Authorization
    request = urllib.request.Request(
        url=SERVER_URL,
        data=data,                       # Body con log en bytes
        headers={
            "Content-Type": "application/json",  # Indicamos que enviamos JSON
            "Authorization": f"Token INVALIDO123"   # Token para validar en el servidor
        },
        method="POST"
    )

    # Ejecutamos la request y leemos la respuesta del servidor
    with urllib.request.urlopen(request) as response:
        resp_body = response.read().decode("utf-8")
        print(f"Respuesta del servidor: {resp_body}")

except urllib.error.HTTPError as e:
    # Error HTTP (por ejemplo 401, 403, 404, 500)
    print(f"[ERROR] HTTP {e.code}: {e.reason}")
except urllib.error.URLError as e:
    # No se pudo conectar al servidor
    print(f"[ERROR] No se pudo conectar al servidor: {e.reason}")
except Exception as e:
    # Otro error inesperado
    print(f"[ERROR] Error inesperado: {e}")