# Importamos socket para conectarnos al servidor:
import socket

# Importamos select para manejar los "hilos" y utilizar menos memoria.
import select

# Importamos sys para manejar directamente el sistema.
import sys

# Importamos random, para que elija uno de los valores al alzar:
import random

# Importamos datetime para que podamos registrar cuando se realizó el log:
from datetime import datetime

# Importamos sqlite3 para conectarnos a nuestra base de datos:
import sqlite3

# Importamos los datos de otros files:
from options_log import services, severities, messages



# Nos conectamos nuestra base de datos:
lista_de_logs = sqlite3.connect("Lista_de_movimientos.db") 

# Creamos nuestro cursor:
cursor = lista_de_logs.cursor()

# Crear socket e intentar conectar
client_socket = socket.socket()
try:
    client_socket.connect(('localhost', 8000))
except ConnectionRefusedError:
    print("No se pudo conectar a ningún servidor. El servidor no debe estar abierto.")
    sys.exit()

# Pedir nombre
print()
nombre_del_cliente = input("Elige tu nombre para este servidor: ")
print()

client_socket.send(nombre_del_cliente.encode("utf-8"))


# Función para generar un log aleatorio
def generar_log_random():
    log = {
        "timestamp": datetime.utcnow().isoformat() + "Z",  # ISO 8601 con zona Zulu (UTC)
        "service": random.choice(services),                # Escoge un servicio aleatorio
        "severity": random.choice(severities),             # Escoge nivel de severidad
        "message": random.choice(messages)                 # Escoge un mensaje
    }
    return log


# Generar 5 logs de ejemplo
for _ in range(5):
    print(generar_log_random())


# Función para enviar un log falso y que el servidor lo deniegue:
def generar_false_log():
    false_log = {
        "timestamp": str(0000) + "Z",       # Convertido a string para dé error
        "service": "testing_service",       # Un servicio inexistente
        "severity": "testing_severity",     # Severidad inválida
        "message": "Soy un mensaje falso"   # Mensaje que no existe en los válidos
    }
    return false_log