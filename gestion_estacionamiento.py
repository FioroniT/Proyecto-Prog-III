import sqlite3


def create_tables(cursor, conn):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            dni INTEGEREGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT
        )
    """)
    #TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UsoEstacionamiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingreso TEXT,
            egreso TEXT NULL,
            usuario INTEGER,
            plaza INTEGER,
            auto TEXT,
            FOREIGN KEY (usuario) REFERENCES Usuarios(dni),
            FOREIGN KEY (plaza) REFERENCES Plaza(numero),
            FOREIGN KEY (auto) REFERENCES Autos(patente)
        )
    """)

    #BOOLEAN no es un tipo de dato aceptado, deberia usarse un INTEGEREGER limitado a 1 o 0
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Plaza (
            numero INTEGER PRIMARY KEY,
            ocupado BOOLEAN,
            techado BOOLEAN,
            ancho FLOAT,
            profundidad FLOAT,
            alto FLOAT
        )
    """)
    conn.commit()
def obtener_plaza(cursor):

    rows = cursor.execute(f'''SELECT numero FROM Plaza WHERE ocupado = 0''').fetchall()
    if len(rows) > 0:
        (a,) = rows[0]
    else:
        a = -1
    return a
def ingresar_vehiculo (cursor, conn, usuario, auto):
    plaza = obtener_plaza(cursor)
    if plaza != -1:
        alta(cursor, conn, '1' , '2' , usuario, plaza,auto)
        (id,) = cursor.execute(f'''SELECT last_insert_rowid()''').fetchall()[0]
        cursor.execute(f'''UPDATE Plaza SET ocupado = 1 WHERE numero = {plaza}''')
        conn.commit()
        print(f'''su numero de tramite es: {id}''')
        return id
    else:
        print("no quedan plzas disponibles")
        return -1

def consultar_tabla(cursor, conn, consulta: str):
    cursor.execute(consulta)
    conn.commit()

def alta(cursor, conn, ingreso, egreso, usuario, plaza, auto):
    #se da de alta un usuario y vehiculo
    cursor.execute(f'''INSERT INTO UsoEstacionamiento (ingreso, egreso, usuario, plaza, auto) VALUES({ingreso}, {egreso}, {usuario}, {plaza}, {auto})''')
    conn.commit()

def retirar_vehiculo(id_ticket, cursor, conn):
    plazas = cursor.execute(f'''SELECT plaza FROM UsoEstacionamiento WHERE id = {id_ticket}''').fetchall()
    if len(plazas) > 0:
        (plaza,) = plazas[0]
        baja(cursor,conn,id_ticket)
        print("se dio de baja")
        cursor.execute(f'''UPDATE Plaza SET ocupado = 0 WHERE numero = {plaza}''')
        conn.commit()
    else:
        print("el ticket no corresponde a una plaza ocupada")

def baja(cursor, conn, id):
    #se da de baja el usuario y vehiculo
    cursor.execute(f'''DELETE FROM UsoEstacionamiento WHERE id = {id}''')
    conn.commit()
    #Parametros a rellenar


def modificar_tabla(cursor, conn, modificacion: str):
    cursor.execute(modificacion)
    conn.commit()

def main():
    id = 23
    ingreso = "'2024-11-01 07:32:00.000'"
    egreso = "'2024-11-02 10:05:00.000'"
    usuario = 123456
    plaza = 1
    auto =  "'ABC 123'"
    #-----------------------------------------------------------------#
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    create_tables(cursor, conn)
#######################################################################
    # metodos de ingreso y egreso de vehiculos

    retirar_vehiculo(8, cursor, conn)
    ingresar_vehiculo(cursor, conn, usuario,auto)

#######################################################################
    conn.close()
    
    

if __name__ == '__main__':
    main()