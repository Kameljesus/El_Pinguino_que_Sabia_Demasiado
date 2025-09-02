import socket
import threading
import sys

lista_de_clientes = [] # Para guardar (nombre, conexion)

def enviar_a_todos(mensaje, cliente_que_envio):
    for nombre, conexion in lista_de_clientes:
        if conexion != cliente_que_envio:  # No enviar al que escribió
            try:
                conexion.send(mensaje.encode("utf-8"))
            except:
                # Si hay error, remover cliente de la lista
                lista_de_clientes.remove((nombre, conexion))

# Creamos el socket del servidor:
server_socket = socket.socket()

try:
    # Establecemos la conexión: La IP, El Puerto para el socket.
    server_socket.bind(('localhost', 8000))
except OSError:
    print("No pueden haber dos servidores iguales con un mismo host y mismo puerto.")
    sys.exit()

# Establecemos la cantidad de conexiones que puede manejar mi socket en cola:
server_socket.listen(5)

# Esta función se ejecutará en un hilo diferente para cada cliente:
def manejar_cliente(conexion, addr):
    global lista_de_clientes
    nombre_del_cliente = conexion.recv(1024).decode("utf-8")
    lista_de_clientes.append((nombre_del_cliente, conexion))
    print()
    print("Nueva Conexión establecida:")
    print(f"{nombre_del_cliente} se ha conectado desde: {addr}")
    print()
    
    while True:
        try:
            mensaje_del_cliente = conexion.recv(1024).decode("utf-8") 

            # Cliente se desconectó (Desconexión normal/abrupta):
            if not mensaje_del_cliente:
                # Remover cliente de la lista
                lista_de_clientes.remove((nombre_del_cliente, conexion))
                print(f"{nombre_del_cliente} se ha desconectado inesperadamente")
                conexion.close()
                break

            # Cliente se desconectó (Desconexión controlada)
            else:
                # Verificar si es comando /exit
                if mensaje_del_cliente.lower() == "/exit":
                    # Remover cliente de la lista
                    lista_de_clientes.remove((nombre_del_cliente, conexion))
                    print(f"{nombre_del_cliente} ha cerrado su conexión")
                    conexion.close()

                    # Verificar si quedan clientes
                    if not lista_de_clientes:
                        print("No quedan clientes conectados. Cerrando servidor...")
                        server_socket.close()
                        sys.exit()
                    break
                
                else:
                    print(f"[{nombre_del_cliente}]: {mensaje_del_cliente}")
                    # Enviar el mensaje a todos los demás clientes
                    mensaje_completo = f"{nombre_del_cliente}: {mensaje_del_cliente}"
                    enviar_a_todos(mensaje_completo, conexion)
                    # Confirmar al que envió
                    conexion.send("Mensaje recibido...".encode("utf-8"))
        
        # Si algo le falló al cliente, para qué seguirá en línea?
        except ConnectionResetError:
            # Remover cliente de la lista
            lista_de_clientes.remove((nombre_del_cliente, conexion))
            print(f"{nombre_del_cliente} se ha desconectado inesperadamente")
            conexion.close()
            
            # Verificar si quedan clientes
            if not lista_de_clientes:
                print("No quedan clientes conectados. Cerrando servidor...")
                server_socket.close()
                sys.exit()
            break 


# Bucle principal para aceptar conexiones
while True:
    try:
        conexion, addr = server_socket.accept()
        # Crear un hilo para manejar cada cliente
        
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, addr))
        hilo_cliente.start()
    
    except:
        break

server_socket.close()
sys.exit(0)  # Salimos del programa completamente