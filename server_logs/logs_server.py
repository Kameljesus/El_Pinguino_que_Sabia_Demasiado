# Importamos socket para conectarnos al servidor:
import socket

# Importamos random, para que elija uno de los valores al alzar:
import random

# Importamos datetime para que podamos registrar cuando se realizó el log:
from datetime import datetime

# Importamos sqlite3 para crear una base de datos:
import sqlite3

# Importamos los datos de otros files:
from client_logs.options_log import services, severities, messages


# Creamos nuestra base de datos (Se crea el archivo, ya que no existe):
lista_de_logs = sqlite3.connect("Lista_de_movimientos.db") 

# Creamos nuestro cursor:
cursor = lista_de_logs.cursor()

# Creamos la tabla de nuestra base de datos:
# NOT NULL: “esta columna siempre debe tener un valor, no puede quedar vacía (NULL)”.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Timestamps TEXT NOT NULL,
    Services TEXT NOT NULL,
    Severity TEXT NOT NULL,
    Messages TEXT NOT NULL
    );
""")