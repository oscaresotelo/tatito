import streamlit as st
import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Proveedores (
        ID_Proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre_Proveedor TEXT,
        Contacto TEXT
    )
''')
conn.commit()

# Función para insertar datos en la tabla
def insertar_proveedor(nombre, contacto):
    cursor.execute('INSERT INTO Proveedores (Nombre_Proveedor, Contacto) VALUES (?, ?)', (nombre, contacto))
    conn.commit()

# Streamlit
st.title("Carga de Proveedores")

nombre_proveedor = st.text_input("Nombre del Proveedor:")
contacto = st.text_input("Contacto:")

if st.button("Guardar"):
    if nombre_proveedor and contacto:
        insertar_proveedor(nombre_proveedor, contacto)
        st.success("Proveedor agregado con éxito.")
    else:
        st.warning("Por favor, complete todos los campos.")

# Mostrar la tabla de Proveedores debajo del formulario
st.subheader("Lista de Proveedores")
proveedores_data = cursor.execute('SELECT * FROM Proveedores').fetchall()

if proveedores_data:
    st.table(proveedores_data)
else:
    st.info("La tabla de proveedores está vacía.")

# Cerrar la conexión a la base de datos al finalizar
conn.close()
