# Importamos sys para manejar directamente el sistema.
import sys

def establecer_conexion_socket_server(server_socket):
    try:
        # Intentamos establecer la conexión: La IP, El Puerto para el socket.
        server_socket.bind(('localhost', 8000))

    # Si sale mal:
    # Error operativo: lo más común en bind, por ejemplo:
    # - El puerto ya está en uso (otro proceso lo ocupa)
    # - Permisos insuficientes (intentar usar puertos < 1024 sin privilegios)
    # - Dirección inválida o interfaz de red no disponible
    except OSError as e:
        print()
        print(f"[ERROR] No se pudo iniciar el servidor: {e}")
        print("Error al establecer servidor. Cerrando programa...")
        sys.exit(1) # El (1) indica que hubo un error critico.

    # Error inesperado: cubre cualquier otra excepción no contemplada
    except Exception as e:
        print()
        print(f"[ERROR] Error inesperado al iniciar el servidor: {e}")
        print("Error al establecer servidor. Cerrando programa...")
        sys.exit(1)

    # Si sale bien:
    else:
        # Establecemos que nuestro socket no sea un bloqueante (necesario para select en un mismo bucle):
        server_socket.setblocking(False)

        # Establecemos la cantidad de conexiones que puede manejar mi socket en cola:
        server_socket.listen()
        print()
        print("Servidor iniciado correctamente en localhost:8000")


def establecer_conexion_socket_client(client_socket):
    try:
        # Intentamos conectarnos al servidor en localhost:8000
        client_socket.connect(('localhost', 8000))

    except OSError as e:
        print()
        print(f"[ERROR] No se pudo conectar al servidor: {e}")
        print("Error crítico al establecer conexión. Cerrando programa...")
        sys.exit(1)

    except Exception as e:
        print()
        print(f"[ERROR] Error inesperado al conectar al servidor: {e}")
        print("Error crítico al establecer conexión. Cerrando programa...")
        sys.exit(1)

    else:
        # No bloqueante, necesario si usas select en el cliente
        client_socket.setblocking(False)
        print()
        print("Conexión al servidor establecida correctamente en localhost:8000")