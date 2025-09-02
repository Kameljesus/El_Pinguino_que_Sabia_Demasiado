import socket
import select
import sqlite3
from datetime import datetime
import json

# Crear server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 y TCP.
server_socket.bind(("localhost", 8000))
server_socket.listen()
server_socket.setblocking(False)

# Lista de sockets a vigilar
sockets_list = [server_socket]

# Lista de clientes: {socket: nombre}
clients = {}

# Conexión a DB
lista_de_logs = sqlite3.connect("Lista_de_movimientos.db")
cursor = lista_de_logs.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamps TEXT NOT NULL,
        services TEXT NOT NULL,
        severity TEXT NOT NULL,
        messages TEXT NOT NULL,
        received_at TEXT
    );
""")
lista_de_logs.commit()

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for s in read_sockets:
        if s == server_socket:
            # Nuevo cliente
            client_socket, addr = server_socket.accept()
            client_socket.setblocking(False)
            sockets_list.append(client_socket)
            # El cliente debe enviar su nombre primero
            nombre = client_socket.recv(1024).decode("utf-8")
            clients[client_socket] = nombre
            print(f"{nombre} se ha conectado desde {addr}")
        else:
            # Cliente ya conectado: recibimos datos
            try:
                data = s.recv(4096)
                if data:
                    # Aquí procesás el log
                    mensaje = data.decode("utf-8")
                    print(f"Log recibido de {clients[s]}: {mensaje}")
                    # INSERTAR EN DB
                    try:
                        log = json.loads(mensaje)
                        received_at = datetime.utcnow().isoformat() + "Z"
                        cursor.execute("""
                            INSERT INTO eventos_logs (timestamps, services, severity, messages, received_at)
                            VALUES (?, ?, ?, ?, ?)
                        """, (log["timestamp"], log["service"], log["severity"], log["message"], received_at))
                        lista_de_logs.commit()
                    except:
                        print("Error al procesar log:", mensaje)
                else:
                    # Cliente cerró conexión
                    print(f"{clients[s]} se ha desconectado")
                    sockets_list.remove(s)
                    del clients[s]
                    s.close()
            except:
                # Cliente desconectado abruptamente
                print(f"{clients[s]} se ha desconectado abruptamente")
                sockets_list.remove(s)
                del clients[s]
                s.close()

    # Manejo de sockets con errores
    for s in exception_sockets:
        sockets_list.remove(s)
        if s in clients:
            del clients[s]
        s.close()
