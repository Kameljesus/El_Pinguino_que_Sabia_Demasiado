"""
http_server.py
Servidor HTTP que recibe logs de clientes y permite consultarlos.
Todo explicado paso a paso.
"""

# -----------------------------
# Importamos librerías
# -----------------------------
from conexion_http import iniciar_servidor_http                                            # Función para iniciar HTTP
from http_db_connect import crear_conectar_db, crear_tabla, crear_log, cargar_log_a_db     # Funciones para la DB
from http_management import LogRequestHandler                                              # Handler que maneja requests POST y GET

# --------------------------------------
# 1) Configuración de la base de datos
# -------------------------------------- 

# 1a) Creamos o conectamos a la base de datos local
lista_de_logs = crear_conectar_db()

# 1b) Creamos el cursor para ejecutar consultas
cursor = crear_tabla(lista_de_logs)

# 1c) Creamos un log inicial para confirmar que la DB está lista
log_inicial = crear_log(
    autor="server",
    service="conexion_db_service",
    severity="INFO",
    mensaje="Base de datos creada y/o conectada correctamente"
)

# 1d) Guardamos el log inicial en la DB
cargar_log_a_db(cursor, lista_de_logs, log_inicial)

# ------------------------------------
# 2) Configuración del servidor HTTP
# ------------------------------------

# 2a) Creamos el servidor y le asignamos nuestro Handler personalizado
server = iniciar_servidor_http(handler_class=LogRequestHandler)

# 2b) Asignamos la conexión a la DB y el cursor al server
# Esto permite que LogRequestHandler acceda a ellos
server.db_conn = lista_de_logs
server.cursor = cursor

# --------------------------------------------
# 3) Inicio del bucle principal del servidor
# --------------------------------------------
print("Servidor listo para recibir logs de clientes...")

try:
    # serve_forever() es un bucle infinito que atiende requests entrantes
    server.serve_forever()
    
except KeyboardInterrupt:
    # Permite cerrar el servidor con Ctrl+C
    print("Servidor detenido por el usuario")

    # Cerramos el socket del servidor
    server.server_close()

    # Cerramos la conexión a la DB
    lista_de_logs.close()