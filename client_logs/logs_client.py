# Importamos socket para conectarnos al servidor:
import socket

# Importamos sys para manejar directamente el sistema.
import sys

# Importamos datetime para que podamos registrar cuando se realizó el log:
from datetime import datetime

# Importamos sqlite3 para conectarnos a nuestra base de datos:
import sqlite3

# Importamos los datos de otros files:
from options_log import services, severities, messages



"""
Socket, select y clientes:
"""

# Crear socket e intentar conectar
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(('localhost', 8000))
except ConnectionRefusedError:
    print("No se pudo conectar a ningún servidor. El servidor no debe estar abierto.")
    sys.exit()

print("Conectado al servidor!")


"""
Base de Datos (DB):
"""

try: # Intentamos conectarnos a nuestra base de datos:
    lista_de_logs = sqlite3.connect("Lista_de_movimientos.db") 

# Si sale mal:
except sqlite3.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
    sys.exit(1)  # Salimos del programa si no hay DB

# Si sale bien:
else:
    # Creamos nuestro cursor:
    cursor = lista_de_logs.cursor()
    print("Conectado a la base de datos con éxito.")



"""
Bucle de manejo de mensajes:
"""

while True:
    try:
        msg = input("Escribe un mensaje: ")
        client_socket.send(msg.encode("utf-8"))

        respuesta = client_socket.recv(1024).decode("utf-8")
        print(f"Servidor: {respuesta}")

    
    except ConnectionResetError:
        client_socket.close()
        # El servidor se desconectó:
        break

    except OSError:
        print("El servidor fue cerrado repentinamente. Ya no se puede enviar más mensajes")
        client_socket.close()
        break