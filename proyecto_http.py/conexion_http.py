# Manejo básico de servidor y cliente HTTP, con funciones separadas y manejo de errores

# Para el servidor HTTP:
from http.server import HTTPServer

# Importamos sys para manejar directamente el sistema.
import sys

# Para el cliente HTTP:
import urllib.request
import urllib.error


# -----------------------------
# Función para iniciar el servidor HTTP
# -----------------------------
def iniciar_servidor_http(host="localhost", puerto=8000, handler_class=None):
    """
    Crea e inicia un servidor HTTP en la IP y puerto indicados.
    handler_class debe ser una subclase de BaseHTTPRequestHandler.
    """
    try:
        server = HTTPServer((host, puerto), handler_class)  # Creamos el servidor
    except OSError as e:
        # Error operativo común: puerto en uso o permisos insuficientes
        print(f"[ERROR] No se pudo iniciar el servidor HTTP: {e}")
        sys.exit(1)  # Salimos con código de error
    except Exception as e:
        # Cualquier otro error inesperado
        print(f"[ERROR] Error inesperado al iniciar el servidor HTTP: {e}")
        sys.exit(1)
    
    # Si sale bien:
    else:
        print(f"Servidor HTTP iniciado correctamente en http://{host}:{puerto}")
        return server


# -----------------------------
# Función para conectarse a un servidor HTTP (cliente)
# -----------------------------
def conectar_servidor_http(url):
    """
    Intenta realizar una conexión simple al servidor HTTP usando GET.
    Sirve para validar que el servidor está disponible.
    """
    try:
        # Creamos la request y abrimos la URL
        respuesta = urllib.request.urlopen(url)
        
    except urllib.error.HTTPError as e:
        # Error de respuesta HTTP (404, 500, etc)
        print(f"[ERROR] El servidor respondió con un error HTTP: {e.code} {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        # Error de conexión, servidor no disponible
        print(f"[ERROR] No se pudo conectar al servidor HTTP: {e.reason}")
        sys.exit(1)
    except Exception as e:
        # Otro error inesperado
        print(f"[ERROR] Error inesperado al conectarse al servidor HTTP: {e}")
        sys.exit(1)
    
    # Si todo sale bien
    else:
        print(f"Conexión exitosa al servidor HTTP: {url}")
        return respuesta.read()  # Podemos leer la respuesta si queremos, atrae los datos reales del servidor