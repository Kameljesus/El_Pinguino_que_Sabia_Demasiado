# Importamos socket para conectarnos al servidor:
import socket

"""
Archivos a ser importados:
"""

from conexion_socket import establecer_conexion_socket

from data_base_connection import crear_conectar_db, cargar_log_a_db

from select_management import vigilar_sockets, nuevo_cliente, recibir_mensaje_del_client

"""
Config.: Socket, select y clientes:
"""

# Creamos el socket del servidor:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectamos nuestro socket:
establecer_conexion_socket(server_socket)

# Establecemos la lista de sockets a vigilar:
sockets_list = [server_socket]

# Lista de clientes: {socket: nombre}:
lista_de_clientes = {}

"""
Base de Datos (DB):
"""

# Conectamos y creamos la DB, obtenemos el objeto conexión
lista_de_logs, cursor = crear_conectar_db()

"""
Bucle de manejo de select:
"""
    
while True:
    read_sockets, exception_sockets = vigilar_sockets(sockets_list, cursor, lista_de_logs)

    # Aquí se procesan nuevos clientes o datos entrantes
    for client_socket in read_sockets:
        if client_socket == server_socket:

            """
            Nuevo cliente:
            """

            conexion, addr = nuevo_cliente(server_socket, sockets_list, cursor, lista_de_logs)
            if conexion is None:
                continue  # O manejar el error de otra manera

            """
            El cliente debe enviar su nombre primero:
            """

            # Recibimos el primer mensaje del cliente (su nombre):
            nombre_del_cliente = recibir_mensaje_del_client(conexion, cursor, lista_de_logs)

            """
            Cargamos el log del nombre a la Base de Datos (DB):
            """

            if nombre_del_cliente is None:
                print(f"Cliente en {addr} no envió nombre o hubo error. Conexión cerrada.")
            else:
                lista_de_clientes[conexion] = nombre_del_cliente
                print()
                print(f"{nombre_del_cliente} se ha conectado desde {addr}")
                cargar_log_a_db(cursor, lista_de_logs, nombre_del_cliente, "sent_text_service", "INFO", nombre_del_cliente)   

            """
            Resto de mensajes del cliente:
            """ 

            mensaje = recibir_mensaje_del_client(conexion)
            if mensaje is None:
                print()
                print(f"{nombre_del_cliente} no envió ningún mensaje o hubo error. Conexión cerrada.")
                sockets_list.remove(client_socket)
                if client_socket in lista_de_clientes:
                    del lista_de_clientes[client_socket]
            else:
                print()
                print(f"{nombre_del_cliente}: {mensaje}")
                cargar_log_a_db(cursor, lista_de_logs, nombre_del_cliente, "sent_text_service", "INFO", mensaje)
            
            """
            Enviar el mensaje a los demás clientes:
            """

            # Enviamos el mensaje a todos los demás clientes conectados
            for other_client in lista_de_clientes:
                if other_client != conexion:  # no enviamos al cliente que lo envió
                    try:
                        # Opcional: podés enviar en formato "Nombre: Mensaje"
                        other_client.send(f"{nombre_del_cliente}: {mensaje}".encode("utf-8"))

                        # Log de envío desde server a otro cliente
                        cargar_log_a_db(cursor, lista_de_logs, "server", "send_text_to_client_service", "INFO", f"Mensaje enviado a {lista_de_clientes[other_client]}")
                    
                    except Exception as e:
                        print()
                        print(f"Error enviando mensaje a {lista_de_clientes[other_client]}: {e}")
                        # Opcional: cerrar la conexión si hay fallo grave
                        other_client.close()
                        sockets_list.remove(other_client)
                        del lista_de_clientes[other_client]