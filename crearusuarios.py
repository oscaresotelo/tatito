""" import sqlite3

# Conectarse a la base de datos (se creará si no existe)
conexion = sqlite3.connect('inventario.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Definir el comando SQL para crear la tabla Usuarios
crear_tabla_sql = '''
CREATE TABLE IF NOT EXISTS Usuarios (
    Usuarios TEXT PRIMARY KEY,
    Password TEXT NOT NULL,
    Nivel INTEGER NOT NULL
)
'''

# Ejecutar el comando SQL para crear la tabla
cursor.execute(crear_tabla_sql)

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()

print("La tabla Usuarios ha sido creada con éxito en tatito.db")
 """
import sqlite3
import streamlit as st

# Función para crear la tabla si no existe
def crear_tabla():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    crear_tabla_sql = '''
    CREATE TABLE IF NOT EXISTS Usuarios (
        Usuarios TEXT PRIMARY KEY,
        Password TEXT NOT NULL,
        Nivel INTEGER NOT NULL
    )
    '''
    
    cursor.execute(crear_tabla_sql)
    conexion.commit()
    conexion.close()

# Inicializar la tabla si no existe
crear_tabla()

# Definir la función para agregar usuarios
def agregar_usuario():
    usuario = st.text_input("Usuario")
    password = st.text_input("Password", type="password")
    nivel = st.number_input("Nivel", min_value=1)

    if st.button("Agregar Usuario"):
        if usuario and password:
            try:
                conexion = sqlite3.connect('inventario.db')
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO Usuarios (Usuarios, Password, Nivel) VALUES (?, ?, ?)", (usuario, password, nivel))
                conexion.commit()
                conexion.close()
                st.success("Usuario agregado con éxito")
            except sqlite3.IntegrityError:
                st.error("El usuario ya existe")
        else:
            st.warning("Por favor, ingresa un usuario y contraseña")

# Crear una sesión para st.session_state
st.title("Alta de Usuarios")
agregar_usuario()
