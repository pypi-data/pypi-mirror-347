def dict_list_to_table(dict_list):
    # Si la lista está vacía, devolver una lista vacía y None como encabezados
    if not dict_list:
        return None, []
    
    # Obtener las claves del primer diccionario para usarlas como encabezados
    columnas = list(dict_list[0].keys())
    
    # Crear la lista para los datos (sin incluir encabezados)
    data = []
    
    # Agregar cada fila de valores
    for item in dict_list:
        # Extraer los valores en el mismo orden que los encabezados
        row = [item.get(header, '') for header in columnas]
        data.append(row)
    
    return  data, columnas

def exists_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    result = cursor.fetchone()
    return result is not None

def create_table(conn, table_name, columnas): 
    cursor = conn.cursor()
    # Crear la tabla con las columnas especificadas
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columnas)});")
    conn.commit()
    print(f"Tabla '{table_name}' creada exitosamente.")
    
def insertar_datos(conn, tabla, data, columnas):   
    # Crear el cursor
    cursor = conn.cursor()
    
    # Construir la sentencia SQL apropiada
    nombres_columnas = ", ".join([f'"{col}"' for col in columnas])
    marcadores = ", ".join(["?" for _ in columnas])
    
    sql = f"INSERT INTO {tabla} ({nombres_columnas}) VALUES ({marcadores})"
    
    # Insertar cada fila de datos
    for fila in data:
        try:
            cursor.execute(sql, fila)
        except Exception as e:
            print(f"Error al insertar fila {fila}: {e}")
    
    # Confirmar los cambios
    conexion.commit()
    print(f"Se insertaron {len(filas)} registros en la tabla {tabla}")