def saludar(nombre):
    return f"Hola, {nombre}! Esta es tu librería personalizada."

def Conector_bbdd(tipo='sqlite', nombre='mi_base_de_datos', host='localhost', puerto=None, usuario=None, password=None):
    """
    Conecta a una base de datos SQL o NoSQL según el tipo especificado.

    Parámetros:
    - tipo: 'sqlite', 'mysql' o 'mongodb'
    - nombre: nombre de la base de datos
    - host, puerto, usuario, contraseña: solo para MySQL y MongoDB

    Retorna:
    - Objeto de conexión (SQLite/MySQL) o cliente (MongoDB)
    """
    if tipo == 'sqlite':
        import sqlite3
        import os
        nombre_db = f"{nombre}.db"     
        conn = sqlite3.connect(nombre_db)
        return conn

    elif tipo == 'mysql':
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            port=3306,
            user=usuario,
            password=password)
            # Crear la base de datos
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre}")
        print(f"Base de datos '{nombre}' creada exitosamente.")
        return conn

    elif tipo == 'mongodb':
        from pymongo import MongoClient
        if puerto is None:
            puerto = 27017
        cliente = MongoClient(host=host, 
                              port=puerto, 
                              username=usuario, 
                              password=password)
        print("Conectado a MongoDB")
        return cliente[nombre]

    else:
        raise ValueError("Tipo de base de datos no soportado. Usa 'sqlite', 'mysql' o 'mongodb'.")

def Cerrar_conexion(conn):
    """
    Cierra la conexión a la base de datos.

    Parámetros:
    - conn: objeto de conexión

    Retorna:
    - None
    """
    if conn:
        conn.close() 
        
def Insert(conn, tabla, data):
   # Verifica el tipo de base de datos con la que estamos trabajando
    import sqlite3
    import mysql.connector
    from pymongo.database import Database 
    
    # Extraer las claves y valores del diccionario
    columnas = data.keys()
    valores = tuple(data.values())
    
    ############# SQLite ################
    if isinstance(conn, sqlite3.Connection):
        print("Conexión exitosa a la base de datos SQL.")
        cursor = conn.cursor()
        
        # Crear la tabla dinámicamente si no existe
        columnas_definicion = ", ".join([f"{col} TEXT" for col in columnas])
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {tabla} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columnas_definicion}
            )
        """)
        print(f"Tabla '{tabla}' verificada o creada exitosamente.")
        
        # Si `data` es un solo diccionario, conviértelo en una lista
        if isinstance(data, dict):
            data = [data]
        # Inserta cada elemento de la lista en la tabla
        for registro in data:
            columnas = ", ".join(registro.keys())
            valores = ", ".join(["?"] * len(registro))
            query = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"
            cursor.execute(query, tuple(registro.values()))
        conn.commit()
        print("Datos insertados correctamente en SQLite.")
        
        # Consulta los datos insertados
        cursor.execute("SELECT * FROM {tabla}")
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"ID: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}")
            
    ############# MySQL ################
    elif isinstance(conn, mysql.connector.connection_cext.CMySQLConnection):
        print("Conexión exitosa a la base de datos MySQL.")
        # Si estamos usando MySQL, podemos trabajar con la conexión de esta manera
        cursor = conn.cursor()
        # Verificar si la tabla 'usuarios' existe y crearla si no
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS {tabla} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                edad INT NOT NULL
            )
        """)
        print("Tabla 'usuarios' verificada o creada exitosamente.")
        # Inserta datos en la tabla 'usuarios'
        cursor.execute("INSERT INTO {tabla} (nombre, edad) VALUES (%s, %s)", data)
        conn.commit()
        print("Datos insertados correctamente en la base de datos MySQL.")

        # Consulta los datos insertados
        cursor.execute("SELECT * FROM usuarios")
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"ID: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}")
            
    ############# MongoDB ################
    elif isinstance(conn, Database):
        print("Conexión exitosa a la base de datos NoSQL.")
        print(conn)
        # Si estamos usando MongoDB, podemos trabajar con la base de datos NoSQL de esta manera
        usuarios = conn["usuarios"]  # Supone que estamos trabajando con la colección 'usuarios'

        # Inserta un documento en la colección
        usuarios.insert_one({"nombre": "Ana", "edad": 25})
        print("Datos insertados correctamente en la base de datos NoSQL.")

        # Consulta los documentos insertados
        for usuario in usuarios.find():
            print(f"Nombre: {usuario['nombre']}, Edad: {usuario['edad']}")