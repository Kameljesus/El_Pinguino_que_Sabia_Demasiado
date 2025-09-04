## socket.socket(socket.AF_INET, socket.SOCK_STREAM):

1. socket.AF_INET:

    - Indica que el socket va a usar IPv4 (direcciones como 127.0.0.1 o 192.168.1.10).
    - Si usaras AF_INET6, sería para IPv6.

2. socket.SOCK_STREAM

    - Define el tipo de socket.

    - SOCK_STREAM significa TCP, que:
        - Es confiable: garantiza que los datos lleguen en orden y completos.
        - Es orientado a conexión: primero se establece la conexión antes de enviar datos.

    - Otra opción sería SOCK_DGRAM → UDP, que no garantiza entrega ni orden, pero es más rápido.


🔹 Analogía rápida:

- AF_INET → “voy a hablar usando direcciones de calle (IPv4)”
- SOCK_STREAM → “voy a mandar cartas en sobres seguros y en orden (TCP)”, en vez de “postales rápidas que pueden perderse (UDP)”


## read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list):

1. select.select()
    - Es la función que revisa qué sockets están listos para ser usados.
    - Permite manejar muchos sockets en un solo hilo sin bloquearse-
    - Toma tres listas de sockets como argumentos:
    
    select.select(read_list, write_list, exception_list)

    - read_list → sockets que queremos vigilar para lectura (datos entrantes o nuevas conexiones).
    - write_list → sockets que queremos vigilar para escritura (cuando están listos para enviar datos sin bloquear).
    - exception_list → sockets que queremos vigilar para errores (conexiones caídas, problemas).

2. Qué hace la línea que puse:

read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

- sockets_list → lista de todos los sockets que queremos revisar.

    - Se pasa como lista de lectura para saber quién tiene datos disponibles (read_list).
    - También se pasa como lista de excepciones para saber quién tiene problemas (exception_list).

- [] → lista vacía de escritura, porque por ahora no nos interesa vigilar quién puede escribir sin bloquearse.
- read_sockets → lista que devuelve todos los sockets que tienen datos listos para leer.
- exception_sockets → lista que devuelve todos los sockets que tienen errores.
- _ → usamos _ para ignorar la lista de sockets listos para escribir.


    # Por qué ignoramos write_list en este caso:

    1. write_list sirve para vigilar qué sockets están listos para enviar datos sin bloquearse.

        - Si un socket no está listo para escribir, un send() podría bloquear el programa (Por ejemplo, si el buffer está lleno).
        - select nos permite saber cuáles podemos escribir de inmediato.

    2. En tu server de logs:

        - Los clientes solo envían logs al servidor (casi todo es lectura para el server).
        - Cuando el server responde, los datos son muy pequeños (por ejemplo "Log recibido").
        - En TCP, sockets generalmente están listos para escribir inmediatamente, así que no necesitamos vigilarlos.

    3. Por eso ponemos [] en la posición de write_list:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    - _ significa: “me importa un carajo qué sockets están listos para escribir por ahora”.
    - Si en el futuro quisieras enviar archivos grandes o mensajes pesados, ahí sí conviene vigilar write_list.


## Parte de HTTP:

# Qué es http.server?:

http.server es una librería estándar de Python para crear servidores HTTP simples, sin instalar nada extra.

Cuando trabajás con http.server en Python, hay dos piezas principales:

1. El servidor HTTP en sí → (HTTPServer)
    
    - Es el que escucha en un puerto (localhost:8000) y espera que lleguen requests.
    - No sabe qué hacer con ellos, solo los recibe.

2. El manejador de requests (Handler) → (BaseHTTPRequestHandler)

Es una clase que define cómo responder a cada request.

Ejemplo: si llega un GET /logs o un POST /logs, el Handler decide qué devolver.

# Qué es HTTPServer?:

Es la clase que representa el servidor HTTP en sí.
Se encarga de:

- Abrir un puerto TCP.
- Esperar conexiones de clientes.
- Pasar cada request al handler para procesarla.

Ejemplo de creación:
server = HTTPServer(("localhost", 8000), MiHandler)

- "localhost" → IP donde corre el servidor.
- 8000 → puerto donde se escucha.
- MiHandler → clase que define cómo responder a GET/POST.

# Qué es BaseHTTPRequestHandler?:

Es la clase base que define cómo manejar las requests HTTP.

Se “hereda” para crear tu propia clase donde defines los métodos:

- do_GET(self) → qué hacer cuando un cliente hace un GET.
- do_POST(self) → qué hacer cuando un cliente hace un POST.

Todo lo que pongas dentro de esos métodos se ejecuta cuando llega una request.

# Qué es un Handler?:

Un Handler es una clase que hereda de BaseHTTPRequestHandler.
En ella, vos sobreescribís métodos como:

- do_GET(self) → lo que hace el servidor cuando alguien manda un GET.
- do_POST(self) → lo que hace el servidor cuando alguien manda un POST.

Ejemplo básico:

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MiHandler(BaseHTTPRequestHandler):  # <- acá definís tu Handler
    def do_GET(self):
        # Configurar respuesta (200 OK)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        # Enviar datos
        respuesta = {"mensaje": "Hola desde el servidor"}
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_POST(self):
        # Leer datos enviados
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        # Log en consola (en un futuro, lo guardás en DB)
        print("Datos recibidos:", post_data.decode("utf-8"))

        # Responder
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

## ¿Por qué usamos BaseHTTPRequestHandler?:

Python no permite “solamente llamar a una función” cada vez que llega un request HTTP.
Necesitamos un handler, que es un objeto que sabe qué hacer cuando llega un POST o GET.

BaseHTTPRequestHandler ya tiene toda la infraestructura:

- Recibe la conexión TCP
- Parseo de headers
- Manejo de errores básicos
- Nos llama a métodos como do_POST y do_GET

Por eso, aunque solo quieras recibir logs, tenés que subclasificar BaseHTTPRequestHandler y definir do_POST (y opcionalmente do_GET).

# Qué es urllib.request?:

urllib.request es una librería estándar de Python para hacer solicitudes HTTP desde Python, sin usar nada externo.

Con ella podés:

- Hacer GET a un servidor:

    import urllib.request
    respuesta = urllib.request.urlopen("http://localhost:8000/logs")
    datos = respuesta.read()

- Hacer POST enviando datos:

    import json
    from urllib import request

    log = {"message": "Hola"}
    req = request.Request(
        "http://localhost:8000/logs",
        data=json.dumps(log).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    response = request.urlopen(req)
    print(response.read())

# Qué es urllib.error?:
urllib.error contiene las excepciones que se lanzan si la request falla.

Por ejemplo:

- HTTPError → el servidor respondió, pero con un error HTTP (404, 500, etc).
- URLError → no se pudo conectar al servidor (no existe, puerto cerrado, etc).

Ejemplo de uso:

import urllib.request, urllib.error

try:
    respuesta = urllib.request.urlopen("http://localhost:8000/logs")
except urllib.error.HTTPError as e:
    print("Error HTTP:", e.code)
except urllib.error.URLError as e:
    print("No se pudo conectar:", e.reason)