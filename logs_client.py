# Importamos socket para conectarnos al servidor:
import socket

"""
Archivos a ser importados:
"""
from conexion_socket import establecer_conexion_socket_client

from data_base_connection import crear_conectar_db, cargar_log_a_db

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
