## Qué es un log?:

Un log es básicamente un registro estructurado de eventos que ocurren en un sistema.

- Puede ser un evento normal (por ejemplo: “usuario inició sesión”)
- O un evento anormal / error (por ejemplo: “falló la conexión a la base de datos”)

Su propósito es documentar todo lo que sucede, para que luego alguien (humano o programa) pueda:

1. Monitorear el estado del sistema.
2. Depurar errores cuando algo falla.
3. Analizar patrones y comportamiento del software.

# Características de un log

- Secuencial: cada entrada tiene un orden cronológico.

- Estructurado: suele tener campos como timestamp, service, severity, message.

- Persistente: se guarda en disco o base de datos para revisarlo después.

- Automático: el sistema genera logs sin intervención manual.

# Estructura:

1️⃣ timestamp:

- Es la fecha y hora exacta en que ocurrió el evento que estás registrando.
- Formato común: ISO 8601, por ejemplo:
  
  2025-08-27T13:45:00Z
  
  donde Z indica UTC (hora universal).

- Sirve para saber cuándo pasó algo, ordenar logs, y aplicar filtros por fecha.


2️⃣ service:

- Sí, es el nombre del servicio que generó el log.
- Ejemplos: "auth_service", "payment_gateway", "notification_service".
- Ayuda a identificar qué parte del sistema produjo el evento.


3️⃣ severity

Es el nivel de importancia del log, o cuán grave es el evento.

Niveles comunes:

- DEBUG → información muy detallada, útil para programadores.
- INFO → información general de eventos normales.
- WARNING → algo inusual pasó, pero no rompe nada.
- ERROR → un error que afecta el funcionamiento.
- CRITICAL → falla grave que necesita atención inmediata.

Esto te permite filtrar por gravedad más adelante (GET /logs?severity=ERROR).


4️⃣ message

Es el texto descriptivo del evento.
Puede ser un mensaje de error, advertencia, o simplemente información de registro.

Ejemplos:

- "Usuario 42 no encontrado"
- "Conexión al servidor de pagos exitosa"
- "Cache miss: producto 123"


Resumiendo: cada log debería verse así en JSON:
{
  "timestamp": "2025-08-27T13:45:00Z",
  "service": "auth_service",
  "severity": "ERROR",
  "message": "Usuario 42 no encontrado"
}


# Analogía sencilla:

Imaginá un diario de bitácora de un barco:

Cada movimiento, cada alerta y cada incidente se anota con fecha y hora.
Si algo sale mal, podés revisar el diario y ver qué pasó, cuándo y dónde.

En tu proyecto:

Cada servicio simulado genera logs.
El servidor central los recibe y los guarda para que después puedas consultarlos o analizarlos.


## ¿Qué es JSON?

JSON (JavaScript Object Notation) es un formato ligero de intercambio de datos que permite que distintos programas y lenguajes se comuniquen de forma entendible.

- Es texto plano, fácil de leer y escribir por humanos.
- Estructurado en pares clave-valor (similar a diccionarios en Python o objetos en JavaScript).
- Muy usado para enviar información entre clientes y servidores en aplicaciones web.

Ejemplo simple:

{
  "timestamp": "2025-08-27T13:45:00Z",
  "service": "auth_service",
  "severity": "ERROR",
  "message": "Usuario 42 no encontrado"
}

- "timestamp" → clave, "2025-08-27T13:45:00Z" → valor
- "service" → clave, "auth_service" → valor
Así para cada campo del log

Características clave:

1. Legible: tanto para humanos como para máquinas.
2. Estandarizado: todos los lenguajes principales saben cómo parsearlo.
3. Flexible: soporta objetos anidados, arrays, números, strings, booleanos y nulos.

En tu proyecto:

- Cada log va a viajar en JSON del cliente al servidor.
- El servidor lo parsea (lee) y lo guarda en la base de datos.


## 🌐 ¿Qué es HTTP?:

HTTP (HyperText Transfer Protocol) es el protocolo que usan casi todos los servicios web para comunicarse.
En simple: es el lenguaje que hablan cliente y servidor en la web.

# Qué es GET?:

GET significa: “obtener”. Se usa para pedir información al servidor, sin modificar nada.

Ejemplo en tu proyecto:

- GET /logs → quiero ver todos los logs, o los que cumplen cierto filtro (timestamp_start, timestamp_end).

Datos que enviás al servidor: solo parámetros en la URL (query string).
Respuesta: el servidor te devuelve lo que pediste.

Analogía: ir a la biblioteca y pedir un libro prestado. No cambias nada, solo lees.

# Qué es POST?:

POST significa “enviar” o “crear”. Se usa para mandar datos al servidor para que haga algo con ellos (guardar, procesar, etc).

Ejemplo en tu proyecto:

- POST /logs → envío un log (JSON) para que el servidor lo guarde en la base de datos.

Datos que enviás: generalmente en el cuerpo del mensaje (body), no en la URL.
Respuesta: el servidor confirma que lo recibió y lo procesó.

Analogía: enviar una carta al servidor diciendo “acá está un nuevo log, guardalo”.



## Qué es un Token?:

Un token en programación (y en este proyecto) es básicamente una llave secreta en forma de texto.

Idea general:

- Imaginá que tenés varios servicios que quieren mandarle logs a tu servidor.

- ¿Cómo sabe el servidor quién es quién y que no le está escribiendo un intruso cualquiera?

- Para eso cada servicio tiene un token único (por ejemplo "abc123XYZ").

Cuando un servicio envía un log, lo acompaña con su token en el header:

Authorization: Token abc123XYZ


El servidor recibe el mensaje y dice:

- ¿Ese token está en mi lista de tokens válidos?

- Si sí → lo acepto y guardo el log.

- Si no → le contesto con un error tipo: {"error": "Quién sos, bro?"}.


En resumen:

- Es un identificador secreto.

- Sirve para autenticar (saber quién es el que manda).

- Y también para autorizar (permitir o negar acceso).

## Qué es un header?:

Un header (cabecera HTTP) es información adicional que se envía antes del cuerpo (body) de una petición o respuesta HTTP.
Sirve para darle contexto al servidor o al cliente sobre lo que viene.

Ejemplo de petición HTTP con headers

Cuando tu cliente hace un POST /logs, no manda solo el JSON. También manda metadatos en el header.

Por ejemplo:

  POST /logs HTTP/1.1
  Host: localhost:8000
  Content-Type: application/json
  Authorization: Token TOKEN123
  Content-Length: 78

  {"autor":"cliente1","service":"test","severity":"INFO","message":"Hola mundo!"}


🔍 Fijate que:

- Host: localhost:8000 → a qué servidor estás hablando.
- Content-Type: application/json → el servidor sabe que el body está en formato JSON.
- Authorization: Token TOKEN123 → tu header personalizado para autenticar al cliente.
- Content-Length: 78 → cuántos bytes tiene el body.


## Qué es un Endpoint?:

Un endpoint es como una puerta de entrada a tu servidor, identificada por una dirección (URL) y un método (GET, POST, etc).

Es un punto final de comunicación entre un cliente y un servidor.

Cada endpoint corresponde a una acción o recurso específico.

# Ejemplo práctico:

Imaginá tu servidor de logging escucha en:

http://localhost:8080


POST /logs
Endpoint para recibir logs.

- Método: POST
- URL: http://localhost:8080/logs
- Cuerpo: JSON con timestamp, service, severity, message

GET /logs
Endpoint para consultar logs.

- Método: GET
- URL: http://localhost:8080/logs
- Parámetros opcionales:
  http://localhost:8080/logs?timestamp_start=2025-08-01&timestamp_end=2025-08-27

En resumen:

El Endpoint es el lugar al que “apunta” la acción”, ya sea enviar datos, pedir información o cualquier operación.

Por ejemplo:

- POST /logs → el cliente “apunta” aquí para enviar logs.
- GET /logs → el cliente “apunta” aquí para pedir logs.

En otras palabras: es el destino de tu mensaje o request dentro del servidor.


## Analogías:

| Concepto | Analogía                                                  |
| -------- | --------------------------------------------------------- |
| HTTP     | Idioma (lenguaje) que usan cliente y servidor para hablar |
| Endpoint | Puerta o destino al que le hablas dentro del servidor     |
| GET/POST | Verbos del idioma, te dicen qué acción querés hacer       |
| Socket   | Tubo o canal por donde viajan las cartas (bytes crudos)   |
| Token    | Llave secreta que demuestra quién sos                     |


# El Cartero y la carta:

Socket (TCP) 👉 es como el cartero + el sobre físico. Es el canal crudo que transporta bytes de un lado a otro.

HTTP 👉 es el idioma y formato de la carta que viaja dentro de ese sobre. Define cómo escribirla para que el que la reciba entienda (dónde está el remitente, asunto, cuerpo del mensaje, etc.).

# Las Llaves de la casa:

Si tu casa tiene llaves distintas para cada persona, vos (el servidor) sabés quién puede entrar y quién no.

El token sería esa llave.

# El Restaurante:

El restaurante entero es tu servidor.

Cada endpoint es una puerta específica:

“/logs” = la puerta donde dejas tus pedidos de logs.

“/stats” = la puerta donde pides estadísticas.

Cuando alguien toca esa puerta (hace una request a ese endpoint), tu servidor tiene que responder con lo que corresponde.