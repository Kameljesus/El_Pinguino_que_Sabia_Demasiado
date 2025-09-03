# Importamos sys para manejar directamente el sistema.
import sys

# Importamos sqlite3 para crear una base de datos:
import sqlite3

# Importamos json para recibir y enviar datos en este formato:
import json

# Importamos datetime para que podamos registrar cuando se realizó el log:
from datetime import datetime


def crear_conectar_db(): # O conectar
    try: # Intentamos crear o conectarnos a nuestra base de datos (Se crea el archivo, si no existe):
        lista_de_logs = sqlite3.connect("Lista_de_movimientos.db")

    # Si sale mal:
    # Error operativo: ocurre si el archivo de DB no puede abrirse o crearse 
    # (ruta inválida, permisos denegados, disco lleno, DB bloqueada, etc.)
    except sqlite3.OperationalError as e:
        print()
        print(f"Error operativo en la base de datos (no se puede abrir o crear el archivo): {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error de base de datos: ocurre si el archivo existe pero está corrupto o ilegible
    except sqlite3.DatabaseError as e:
        print()
        print(f"Error de base de datos (archivo corrupto o ilegible): {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error de interfaz: problemas con cómo SQLite interpreta los parámetros o API de conexión
    except sqlite3.InterfaceError as e:
        print()
        print(f"Error de interfaz con la base de datos: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error general de SQLite: cualquier otro error no específico cubierto por SQLite
    except sqlite3.Error as e:
        print()
        print(f"Error general de SQLite: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error inesperado: algo ajeno a SQLite (problema del sistema, memoria, etc.)
    except Exception as e:
        print()
        print(f"Error inesperado al conectar con la base de datos: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Si sale bien:
    else:
        print()
        print("Conectado a la base de datos con éxito.")

        # Retornamos la lista de logs:
        return lista_de_logs 


def crear_tabla(lista_de_logs):
    # Creamos nuestro cursor:
    cursor = lista_de_logs.cursor()
    print()
    print("Conectado a la base de datos con éxito.")


    try: # Intentamos crear la tabla de nuestra base de datos:
        # NOT NULL: “esta columna siempre debe tener un valor, no puede quedar vacía (NULL)”.
        # received_at es opcional y servirá para saber cuándo el server recibe el log.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor TEXT NOT NULL,
            timestamps TEXT NOT NULL,
            services TEXT NOT NULL,
            severity TEXT NOT NULL,
            messages TEXT NOT NULL,
            received_at TEXT
            );
        """)

    # Si sale mal:
    # Error operativo: ocurre si la DB está bloqueada, no se puede escribir, 
    # o hay un fallo de E/S al guardar los cambios
    except sqlite3.OperationalError as e:
        print()
        print(f"Error operativo en la base de datos al crear la tabla: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error de integridad: aunque raro en un commit vacío, puede darse si algún 
    # cambio viola restricciones de la DB
    except sqlite3.IntegrityError as e:
        print()
        print(f"Error de integridad al crear la tabla: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error de base de datos: problemas de corrupción o inconsistencias al confirmar cambios
    except sqlite3.DatabaseError as e:
        print()
        print(f"Error de base de datos (archivo corrupto o ilegible) al crear la tabla: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error general de SQLite: cualquier otro error no contemplado arriba
    except sqlite3.Error as e:
        print()
        # Cubre cualquier otro error de SQLite no específico
        print(f"Error general de SQLite al crear la tabla: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Error inesperado: problemas fuera de SQLite (fallo de sistema, interrupción, etc.)
    except Exception as e:
        print()
        # Por si surge un error inesperado fuera de SQLite
        print(f"Error inesperado al crear la tabla: {e}")
        print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
        sys.exit(1)

    # Si sale bien:
    else:
        try: # Intentamos insertar la tabla en mi base de datos:
            # Confirmamos los cambios en la base de datos:
            lista_de_logs.commit()
        
        # Si sale mal:
        # Error operativo: por ejemplo, la base de datos está bloqueada o hay problemas de escritura
        except sqlite3.OperationalError as e:
            print()
            print(f"Error operativo al hacer commit en la base de datos: {e}")
            print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
            sys.exit(1)

        # Error de integridad: violación de restricciones (aunque raro en commit de tabla vacía)
        except sqlite3.IntegrityError as e:
            print()
            print(f"Error de integridad al hacer commit: {e}")
            print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
            sys.exit(1)

        # Error general de SQLite
        except sqlite3.DatabaseError as e:
            print()
            print(f"Error de base de datos al hacer commit: {e}")
            print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
            sys.exit(1)

        # Otro error de SQLite que no esté en las categorías anteriores
        except sqlite3.Error as e:
            print()
            print(f"Error general de SQLite al hacer commit: {e}")
            print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
            sys.exit(1)

        # Cubre cualquier error inesperado que no sea de SQLite
        except Exception as e:
            print()
            print(f"Error inesperado al confirmar cambios en la DB: {e}")
            print("Error en la Base de Datos, integridad de logs comprometida. Cerrando programa...")
            sys.exit(1)
        
        # Si sale bien:
        else:
            print()
            print("Base de datos cargada y actualizada con éxito")

            # Retomamos el cursor:
            return cursor


def cargar_log_a_db(cursor, lista_de_logs, autor, service, severity, mensaje):
    try:
        # Convertimos el mensaje JSON a dict
        log = json.loads(mensaje)
        received_at = datetime.utcnow().isoformat() + "Z"

        # Insertamos los datos en la tabla
        cursor.execute("""
            INSERT INTO eventos_logs (autor, timestamps, services, severity, messages, received_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            log.get("autor", autor),
            log.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            log.get("service", service),
            log.get("severity", severity),
            log.get("message", mensaje),
            received_at
        ))

        # Confirmamos los cambios en la base de datos
        lista_de_logs.commit()

    # Error de formato JSON
    except json.JSONDecodeError as e:
        print()
        print(f"Error crítico: mensaje no es JSON válido: {mensaje} -> {e}")
        sys.exit(1)

    # Error operativo SQLite: por ejemplo, base de datos bloqueada o problemas de escritura
    except sqlite3.OperationalError as e:
        print()
        print(f"Error crítico operativo en la DB al guardar log: {e}")
        sys.exit(1)

    # Error de integridad SQLite: violación de restricciones (aunque raro en este caso)
    except sqlite3.IntegrityError as e:
        print()
        print(f"Error crítico de integridad en la DB al guardar log: {e}")
        sys.exit(1)

    # Error general de SQLite
    except sqlite3.DatabaseError as e:
        print()
        print(f"Error crítico de base de datos al guardar log: {e}")
        sys.exit(1)

    # Otro error SQLite no específico
    except sqlite3.Error as e:
        print()
        print(f"Error crítico general de SQLite al guardar log: {e}")
        sys.exit(1)

    # Cubre cualquier otro error inesperado
    except Exception as e:
        print()
        print(f"Error crítico inesperado al guardar log: {e}")
        sys.exit(1)

    # Si sale bien
    else:
        print("Log cargado en DB con éxito")