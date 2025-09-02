# Importamos socket para conectarnos al servidor:
import socket

# Importamos sys para manejar directamente el sistema.
import sys

# Importamos select para manejar los "hilos" y utilizar menos memoria.
import select

# Importamos json para recibir y enviar datos en este formato:
import json

# Importamos datetime para que podamos registrar cuando se realizó el log:
from datetime import datetime

# Importamos sqlite3 para crear una base de datos:
import sqlite3

# Importamos los datos de otros files:
from options_log import services, severities, messages



"""
Socket, select y clientes:
"""

# Creamos el socket del servidor:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Intentamos establecer la conexión: La IP, El Puerto para el socket.
    server_socket.bind(('localhost', 8000))

except OSError as e:
    print()
    print(f"[ERROR] No se pudo iniciar el servidor: {e}")
    print("Error al establecer servidor. Cerrando programa...")
    sys.exit(1) # El (1) indica que hubo un error critico.

# Establecemos que nuestro socket no sea un bloqueante (necesario para select en un mismo bucle):
server_socket.setblocking(False)

# Establecemos la cantidad de conexiones que puede manejar mi socket en cola:
server_socket.listen()

# Establecemos la lista de sockets a vigilar:
sockets_list = [server_socket]

# Lista de clientes: {socket: nombre}:
lista_de_clientes = {}



"""
Base de Datos (DB):
"""
try: # Intentamos crear o conectarnos a nuestra base de datos (Se crea el archivo, si no existe):
    lista_de_logs = sqlite3.connect("Lista_de_movimientos.db")

# Si sale mal:
except sqlite3.OperationalError as e:
    print()
    print(f"Error operativo en la base de datos (no se puede abrir o crear el archivo): {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except sqlite3.DatabaseError as e:
    print()
    print(f"Error de base de datos (archivo corrupto o ilegible): {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except sqlite3.InterfaceError as e:
    print()
    print(f"Error de interfaz con la base de datos: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except sqlite3.Error as e:
    print()
    # Cubre cualquier otro error de SQLite no específico
    print(f"Error general de SQLite: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except Exception as e:
    print()
    # Por si surge un error inesperado fuera de SQLite
    print(f"Error inesperado al conectar con la base de datos: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

# Si sale bien:
else:
    # Creamos nuestro cursor:
    cursor = lista_de_logs.cursor()
    print()
    print("Conectado a la base de datos con éxito.")


try: # Intentamos crear la tabla de nuestra base de datos:
    # NOT NULL: “esta columna siempre debe tener un valor, no puede quedar vacía (NULL)”.
    # received_at es opcional y servirá para saber cuándo el server recibe el log.
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

# Si sale mal:
except sqlite3.OperationalError as e:
    print()
    print(f"Error operativo en la base de datos al crear la tabla: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except sqlite3.IntegrityError as e:
    print()
    print(f"Error de integridad al crear la tabla: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except sqlite3.DatabaseError as e:
    print()
    print(f"Error de base de datos (archivo corrupto o ilegible) al crear la tabla: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except sqlite3.Error as e:
    print()
    # Cubre cualquier otro error de SQLite no específico
    print(f"Error general de SQLite al crear la tabla: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

except Exception as e:
    print()
    # Por si surge un error inesperado fuera de SQLite
    print(f"Error inesperado al crear la tabla: {e}")
    print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
    sys.exit(1)

# Si sale bien:
else:
    try: # Intentamos insertar la tabla en mi base de datos:
        # Confirmamos los cambios en la base de datos:
        lista_de_logs.commit()
    
    # Si sale mal:
    # Error operativo: por ejemplo, la base de datos está bloqueada o hay problemas de escritura
    except sqlite3.OperationalError as e:
        print()
        print(f"Error operativo al hacer commit en la base de datos: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error de integridad: violación de restricciones (aunque raro en commit de tabla vacía)
    except sqlite3.IntegrityError as e:
        print()
        print(f"Error de integridad al hacer commit: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error general de SQLite
    except sqlite3.DatabaseError as e:
        print()
        print(f"Error de base de datos al hacer commit: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Otro error de SQLite que no esté en las categorías anteriores
    except sqlite3.Error as e:
        print()
        print(f"Error general de SQLite al hacer commit: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Cubre cualquier error inesperado que no sea de SQLite
    except Exception as e:
        print()
        print(f"Error inesperado al confirmar cambios en la DB: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)
    
    # Si sale bien:
    else:
        print()
        print("Base de datos cargada y actualizada con éxito")
    



"""
Bucle de manejo de select:
"""

while True:
    try:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Si sale mal:
    except ValueError as e:
        print()
        print(f"Error de valor en select (socket inválido en la lista): {e}")

    except OSError as e:
        print()
        print(f"Error operativo en select (problema con el sistema o conexión de socket): {e}")

    except Exception as e:
        print()
        print(f"Error inesperado al vigilar los sockets (select): {e}")

   # Si sale bien:
    else:
        for client_socket in read_sockets:
                if client_socket == server_socket:

                    """
                    Nuevo cliente:
                    """
                    try: # Intentamos aceptar la conexión del cliente:
                        conexion, addr = server_socket.accept()
                    
                    # Si sale mal:
                    except OSError as e:
                        print()
                        print(f"No se pudo aceptar la nueva conexión: {e}")

                    # Si sale bien:
                    else:
                        # La establecemos como NO bloqueante:
                        conexion.setblocking(False)
                        # Lo agregamos a la lista de sockets:
                        sockets_list.append(conexion) 


                    """
                    El cliente debe enviar su nombre primero:
                    """
                    try: # Intentamos recibir su nombre (mensaje):
                        nombre_del_cliente = conexion.recv(1024).decode("utf-8")
                    
                    # Si sale mal:
                    except Exception as e:
                        print()
                        print(f"No se pudo recibir el nombre del cliente: {e}")
                        conexion.close()

                    # Si sale bien:
                    else:
                        # Lo añadimos a la lista de nombre de clientes:
                        lista_de_clientes[conexion] = nombre_del_cliente
                        # Comprobamos en consola:
                        print()
                        print(f"{nombre_del_cliente} se ha conectado desde {addr}")
                    

                    """
                    Cargamos el log del nombre a la Base de Datos (DB):
                    """
                    try: # Intentamos insertar los datos del log en la DB:
                        log = json.loads(nombre_del_cliente)
                        received_at = datetime.utcnow().isoformat() + "Z"
                        cursor.execute("""
                            INSERT INTO eventos_logs (timestamps, services, severity, messages, received_at)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            log.get("timestamp", "N/A"),
                            log.get("service", "unknown"),
                            log.get("severity", "INFO"),
                            log.get("message", ""),
                            received_at
                        ))

                    # Si sale mal:
                    except Exception as e:
                        print()
                        print(f"Error al insertar los datos del log a la DB: {mensaje} -> {e}")

                    else: # Si sale bien:
                        try:
                            # Confirmamos los cambios en la base de datos:
                            lista_de_logs.commit()
                        
                        # Si sale mal:
                        except sqlite3.Error as e:
                            print()
                            print(f"Error al subir los cambios a la base de datos: {e}")
                        
                        # Si sale bien:
                        else:
                            print()
                            print("Datos cargados con éxito")
                        

                else:
                    # Cliente ya conectado: recibimos datos
                    try:
                        data = client_socket.recv(4096)
                        
                        if data:
                            # Aquí procesás el log
                            mensaje = data.decode("utf-8")
                            print(f"Log recibido de {lista_de_clientes[client_socket]}: {mensaje}")
                            
                            # INSERTAR EN DB
                            try:
                                log = json.loads(mensaje)
                                received_at = datetime.utcnow().isoformat() + "Z"
                                cursor.execute("""
                                    INSERT INTO eventos_logs (timestamps, services, severity, messages, received_at)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (log["timestamp"], log["service"], log["severity"], log["message"], received_at))
                            
                            except Exception as e:
                                print()
                                print("Error al procesar log:", mensaje)
                            
                            else: # Si sale bien:
                                try:
                                    # Confirmamos los cambios en la base de datos:
                                    lista_de_logs.commit()
                                
                                # Si sale mal:
                                except sqlite3.Error as e:
                                    print()
                                    print(f"Error al subir los cambios a la base de datos: {e}")
                                
                                # Si sale bien:
                                else:
                                    print()
                                    print("Datos cargados con éxito")
                        

                        else:
                            # Cliente cerró conexión:
                            print()
                            print(f"{lista_de_clientes[client_socket]} se ha desconectado")
                            sockets_list.remove(client_socket)
                            del lista_de_clientes[client_socket]
                            client_socket.close()
                    
                    except Exception as e:
                        # Cliente desconectado abruptamente:
                        print()
                        print(f"{lista_de_clientes[client_socket]} se ha desconectado abruptamente")
                        sockets_list.remove(client_socket)
                        del lista_de_clientes[client_socket]
                        client_socket.close()