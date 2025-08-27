# Importamos socket para conectarnos al servidor:
import socket

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


# Función para generar un log aleatorio
def generar_log_random():
    log = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": random.choice(services),
        "severity": random.choice(severities),
        "message": random.choice(messages)
    }
    return log


# Generar 5 logs de ejemplo
for _ in range(5):
    print(generar_log_random())


# Función para enviar un log falso y que el servidor lo deniegue:
def generar_false_log():
    false_log = {
        "timestamp": 0000 + "Z",
        "service": "testing_service",
        "severity": "testing_severity",
        "message": "Soy un mensaje falso"
    }
    return false_log