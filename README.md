# El Pingüino que Sabía Demasiado

Proyecto de **cliente-servidor HTTP en Python** que simula un sistema de logging.  
El servidor recibe logs de múltiples clientes vía **HTTP puro** (sin frameworks), los valida y los guarda en una **base de datos**, permitiendo consultas posteriores.

Este proyecto demuestra comprensión de:

- Protocolo HTTP básico (GET/POST)  
- Diseño de clientes y servidores  
- Persistencia en base de datos (SQLite)  
- Autenticación simple mediante tokens  

---

## 🧠 Objetivo del proyecto

- Crear un **servidor HTTP** capaz de recibir y almacenar logs  
- Permitir que **clientes envíen logs simulados** mediante requests HTTP  
- Guardar los logs en una **base de datos SQLite**  
- Validar la autenticidad de los clientes con **tokens**  
- Ejecutar consultas sobre la base para monitoreo y análisis

---

## 🛠️ Tecnologías y herramientas

- 🐍 Python 3  
- 🗄 SQLite (base de datos)  
- 📡 HTTP “crudo” usando librerías de la estándar (`http.server`)  
- 🔑 Autenticación por tokens  
- 📦 Módulos personalizados: `conexion_http.py`, `http_db_connect.py`, `http_management.py`

---

## 📂 Estructura del proyecto

Archivos principales:

- `http_server.py` — Servidor HTTP que recibe logs  
- `http_client.py` — Cliente que envía logs al servidor  
- `http_db_connect.py` — Funciones para crear la DB, insertar logs y consultar  
- `conexion_http.py` — Funciones auxiliares para iniciar el servidor HTTP  
- `http_management.py` — Handler personalizado para manejar requests POST y GET  
- `tokens.py` — Diccionario de tokens válidos para autenticación  
- `venv/` — Entorno virtual  
- `.gitignore`

---

## 🚀 Cómo usar el proyecto

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Kameljesus/El_Pinguino_que_Sabia_Demasiado.git
cd El_Pinguino_que_Sabia_Demasiado/proyecto_http
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv venv
```

Activar el entorno:

  Windows:
  ```bash
  venv\Scripts\activate
  ```

  macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3️⃣ Instalar dependencias

Instalar librerías necesarias (si las hay).
Como se usa solo librerías estándar de Python, esto puede estar vacío, salvo que quieras usar módulos adicionales.

### 4️⃣ Iniciar el servidor

```bash
python http_server.py
```

El servidor iniciará y quedará escuchando requests HTTP entrantes:
```nginx
Servidor listo para recibir logs de clientes...
```

### 5️⃣ Ejecutar clientes

```bash
python http_client.py
```
Los clientes enviarán logs simulados al servidor vía POST HTTP.

### 📊 Ejemplos de logs

Cada log tiene campos como:

- autor — quien envía el log
- service — nombre del servicio emisor
- severity — nivel de log (INFO, WARNING, ERROR)
- mensaje — contenido del log
- timestamp — hora de envío

El servidor guarda todos los logs en la base de datos y permite consultarlos mediante queries SQL.

### 🔒 Autenticación por tokens

Los clientes deben enviar un token válido definido en tokens.py para que el servidor acepte los logs:
```python
VALID_TOKENS = {
    "TOKEN123": "loggin_service",
    "TOKEN456": "send_text_service",
    "TOKEN789": "recive_text_service"
}
```

### 📌 Consultas y análisis de logs

Ejemplos de consultas SQL sobre la base SQLite:
```sql
-- Obtener todos los logs
SELECT * FROM logs;

-- Filtrar logs por nivel de severidad
SELECT * FROM logs WHERE severity='ERROR';

-- Contar logs por servicio
SELECT service, COUNT(*) FROM logs GROUP BY service;
```
