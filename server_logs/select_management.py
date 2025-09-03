# Importamos select para manejar los "hilos" y utilizar menos memoria.
import select

# Importamos la función de registrar log para registrar todos los errores posibles:
from data_base_connection import cargar_log_a_db

def vigilar_sockets(sockets_list, cursor, lista_de_logs):
    try:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Si sale mal:
    # Error de valor: ocurre si en la lista hay algo que no es un socket válido,
    # por ejemplo un objeto cerrado o un tipo incorrecto.
    except ValueError as e:
        print()
        print(f"Error de valor en select (socket inválido en la lista): {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "socket_service", "BUG", f"Error de valor en select: {e}") 

    # Error operativo: puede deberse a problemas del sistema, como que un socket
    # se desconecte de forma abrupta, fallos de red, o errores en el descriptor de archivo.
    except OSError as e:
        print()
        print(f"Error operativo en select (problema con el sistema o conexión de socket): {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "socket_service", "BUG", f"Error operativo en select: {e}")

    # Error inesperado: cubre cualquier otra excepción no contemplada anteriormente,
    # ya sea por un bug en el código o un fallo poco común en la librería select.
    except Exception as e:
        print()
        print(f"Error inesperado al vigilar los sockets (select): {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "socket_service", "CRITICAL", f"Error inesperado en select: {e}")

    # Si sale bien, retornamos los sockets listos
    else:
        return read_sockets, exception_sockets
    
    # Si ocurre un error, retornamos None explícitamente
    return None, None


def nuevo_cliente(server_socket, sockets_list, cursor, lista_de_logs):
    try: # Intentamos aceptar la conexión del cliente:
        conexion, addr = server_socket.accept()

    # Si sale mal:
    # Error de valor: algo muy raro, como un retorno inesperado en la tupla (conexion, addr)
    except ValueError as e:
        print()
        print(f"Error de valor al aceptar conexión (retorno inesperado de accept): {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "socket_service", "BUG", f"Error de valor en accept: {e}")

    # Error operativo: lo más común, por ejemplo:
    # - el socket no está en estado de escucha
    # - recursos del sistema agotados (muchas conexiones abiertas)
    # - conexión interrumpida en el momento de aceptar
    except OSError as e:
        print()
        print(f"Error operativo al aceptar nueva conexión: {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "socket_service", "ERROR", f"Error operativo en accept: {e}")

    # Cubre cualquier otro error inesperado no contemplado arriba
    except Exception as e:
        print()
        print(f"Error inesperado al aceptar nueva conexión: {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "socket_service", "CRITICAL", f"Error inesperado en accept: {e}")

    # Si sale bien:
    else:
        # La establecemos como NO bloqueante:
        conexion.setblocking(False)
        # Lo agregamos a la lista de sockets:
        sockets_list.append(conexion)
        # Retornamos los valores:
        return conexion, addr
    
    # Si ocurre un error, retornamos None explícitamente
    return None, None


def recibir_mensaje_del_client(conexion, cursor, lista_de_logs):
    try: # Intentamos recibir su nombre (mensaje):
        mensaje = conexion.recv(1024).decode("utf-8")
    
    # Si sale mal:
    # Error de conexión: ocurre si el cliente cierra la conexión de forma abrupta
    # antes de enviar su nombre, o si el socket está roto.
    except ConnectionResetError as e:
        print()
        print(f"Error de conexión: el cliente cerró la conexión antes de enviar su mensaje: {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "recv_message_service", "ERROR", f"Conexión cerrada antes de enviar mensaje: {e}")
        conexion.close()
    
    # Error de decodificación UTF-8: sucede si el cliente envía datos que no son UTF-8 válidos.
    except UnicodeDecodeError as e:
        print()
        print(f"[ERROR] Datos recibidos no son UTF-8 válidos: {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "recv_message_service", "BUG", f"Error decodificación UTF-8: {e}")
        conexion.close()

    # Error operativo: puede deberse a problemas en la red o en el socket mismo
    # al intentar recibir datos.
    except OSError as e:
        print()
        print(f"Error operativo al recibir el mensaje del cliente: {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "recv_message_service", "ERROR", f"Error operativo al recibir mensaje: {e}")
        conexion.close()

    # Error inesperado: cubre cualquier otro fallo no contemplado anteriormente.
    except Exception as e:
        print()
        print(f"No se pudo recibir el mensaje del cliente: {e}")
        cargar_log_a_db(cursor, lista_de_logs, "server", "recv_message_service", "CRITICAL", f"Error inesperado en recv: {e}")
        conexion.close()

    # Si todo sale bien, retornamos el mensaje
    else:
        return mensaje
    
    # Si ocurre un error, retornamos None explícitamente
    return None