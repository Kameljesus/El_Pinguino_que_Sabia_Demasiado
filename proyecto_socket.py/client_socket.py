# Importamos socket para conectarnos al servidor:
import socket

# Importamos sys para manejar directamente el sistema.
import sys

"""
Archivos a ser importados:
"""
from conexion_socket import establecer_conexion_socket_client

from data_base_connection import crear_conectar_db, cargar_log_a_db

from select_management import mandar_mensaje, recibir_mensaje

"""
Socket, select y clientes:
"""

# Crear socket:
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectamos nuestro socket:
establecer_conexion_socket_client(client_socket)

"""
Base de Datos (DB):
"""

# Conectamos y creamos la DB, obtenemos el objeto conexión>
lista_de_logs = crear_conectar_db()
cursor = lista_de_logs.cursor()

"""
Bucle de manejo de mensajes:
"""

# Pedir nombre>
print()
nombre_del_cliente = input("Elige tu nombre para este servidor: ")
# Enviamos nombre:
mandar_mensaje(client_socket, nombre_del_cliente, cursor, lista_de_logs, nombre_del_cliente)

# Resto de mensajes:
# Bucle principal
while True:
    # Primero intentamos recibir mensajes del servidor
    mensaje_server = recibir_mensaje(client_socket, cursor, lista_de_logs)

    if mensaje_server is None:  # <- conexión cerrada o error
        print("[INFO] El servidor cerró la conexión o ocurrió un error crítico.")
        cargar_log_a_db(cursor, lista_de_logs, nombre_del_cliente, "server_close_service", "INFO", "Servidor cerró la conexión o error crítico")
        client_socket.close()
        sys.exit(0)

    if mensaje_server:
        print(f"{mensaje_server}")
        cargar_log_a_db(cursor, lista_de_logs, nombre_del_cliente, "send_global_message_service", "INFO", "Mensaje de otro cliente recibido")

    # Luego pedimos al usuario que escriba algo
    mensaje = input("> ")
    if mensaje == "/salir" or mensaje == "/exit":
        print("[INFO] Cerrando cliente...")
        client_socket.close()
        cargar_log_a_db(cursor, lista_de_logs, nombre_del_cliente, "session_close_service", "INFO", "Desconexión controlada")
        sys.exit(0)

    mandar_mensaje(client_socket, mensaje, cursor, lista_de_logs, nombre_del_cliente)