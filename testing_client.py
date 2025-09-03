import socket
import threading
import sys

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


# Hilo de Recepción:
# Función para recibir mensajes del servidor:
def recibir_mensajes():
    while True:
        try:
            mensaje_del_servidor = client_socket.recv(1024).decode("utf-8")

            if not mensaje_del_servidor:  # Servidor cerrado
                print("El servidor fue cerrado repentinamente. Ya no se puede enviar más mensajes")
                client_socket.close()
                sys.exit()

            if mensaje_del_servidor == "Mensaje recibido...":
                print("Visto")
                print()
            
            else:
                print(mensaje_del_servidor)
                print()
        
        except ConnectionResetError:
            # Error de conexión - servidor cerrado
            print("El servidor fue cerrado repentinamente. Ya no se puede enviar más mensajes")
            client_socket.close()
            sys.exit()

# Lanzamos el hilo que escucha los mensajes entrantes
hilo_receptor = threading.Thread(target=recibir_mensajes, daemon=True)
hilo_receptor.start()


# === HILO PRINCIPAL: envía mensajes ===
print("Conectado al servidor. Escribe un mensaje (o '/exit' para salir):")

# Bucle infinito para enviar mensajes:
# Hilo de Emisión:
# Función para mandar mensajes al servidor
while True:
    try:
        mensaje = input()
        
        if mensaje.lower() == "/exit":
            client_socket.send(mensaje.encode("utf-8"))
            print("Desconectando del servidor...")
            client_socket.close()
            sys.exit()

        else:
            # Borrar la línea del input y mostrar el mensaje formateado
            print(f"\033[1A\033[2K{nombre_del_cliente}: {mensaje}")
            print("Enviado")
            client_socket.send(mensaje.encode("utf-8"))
    
    except ConnectionResetError:
        client_socket.close()
        # El servidor se desconectó:
        break

    except OSError:
        print("El servidor fue cerrado repentinamente. Ya no se puede enviar más mensajes")
        client_socket.close()
        break