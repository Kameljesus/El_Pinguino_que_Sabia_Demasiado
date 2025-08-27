# Pseudocódigo:

"""
✅ Servicios simulados que generan logs y los envían por HTTP.

1. Generar logs simulados (o falsos).
2. Guardar esos logs en una base de datos: cúal log?, cuándo?, dónde (tiempo)?, etc.
3. Hacer que esos logs se puedan enviar vía HTTP.

✅ Un servidor central de logging que recibe, valida, guarda y devuelve logs.

1. Crear un server.
2. Vincular a una base de datos para cuando el cliente se registre.
3. Crear un "cliente".
4. Hacer que el cliente se registre y mande los datos al server.

✅ Autenticación con tokens para que no se cuele ningún log anónimo.

1. Recibir los datos del cliente (su mensaje).
2. Verificar sus datos con la lista de logs si son o no, correctos.

✅ Endpoint /logs para recibir y consultar logs, con filtros por fecha.

1. Cuando el cliente haga un get de uno o más logs, este le aparezca con fecha y tiempo en específico.


✅ Todo guardado en base de datos, no en tus sueños.

1. Creamos una base de datos para guardar todos los logs y token.

"""


# Recomendaciones y tips:

"""
🔹 Servicios simulados que generan logs

Excelente que hayas definido: generar logs → guardar → enviar.

Sugerencia: en la fase inicial, podés guardar los logs en memoria primero, para probar el flujo, y luego pasarlos a la DB.

Cada log debería tener al menos: timestamp, service, severity, message.


🔹 Servidor central de logging

Perfecto tener “server” + “cliente” + DB.

Tip: el cliente no debería registrarse directamente en la DB; primero envía su token, y el servidor valida si ese token está en la lista de tokens válidos.

La idea de “cliente se registra y manda los datos” puede confundirse con la fase de autenticación: vos vas a validar tokens, no “registrar clientes” todavía, salvo que quieras hacerlo como bonus más adelante.


🔹 Autenticación con tokens

Muy bien que lo definiste como verificación de datos del cliente.

Precisión: el servidor chequea el token, no la lista de logs. La lista de logs guarda los logs, la lista de tokens guarda quién está autorizado.


🔹 Endpoint /logs con filtros

Correcto, que GET devuelva los logs filtrados por fecha.

Tip: también podés filtrar por service o severity, para hacer la consulta más flexible.

Considera que el cliente manda la petición y el servidor tiene que parsear la URL o parámetros para aplicar filtros.


🔹 Todo guardado en DB

Perfecto, ya lo incluíste.

Tip: para tu proyecto inicial, una sola tabla logs puede bastar, y otra tabla o estructura en memoria para los tokens.



✅ Resumen de mejoras

Diferenciar lista de tokens de la tabla de logs.

Validación de token → server decide si acepta o no los logs.

Filtros: fecha + opcionalmente service/severity.

Podés empezar con memoria antes de la DB para testear flujo básico.
"""