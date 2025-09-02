# socket.socket(socket.AF_INET, socket.SOCK_STREAM):

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


# read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list):

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


    ## Por qué ignoramos write_list en este caso:

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

