import streamlit as st
import sqlite3
from st_pages import Page, show_pages, add_page_title
import base64
# Connect to the SQLite database
conn = sqlite3.connect("inventario.db")
LOGO_IMAGE = "./imagenes/tatito.jpeg"
# Create a cursor
c = conn.cursor()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
                     .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:30px !important;
                color: black !important;
                padding-top: 50px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """
st.markdown(hide_st_style, 

    unsafe_allow_html=True)
    
st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" > <br>
        <p class="logo-text">Movimiento <br> de Inventario</p>
    </div>
    """,
    unsafe_allow_html=True
)

if "ingreso" not in st.session_state:
      st.session_state.ingreso = ""

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def login():
    st.session_state.ingreso = "ok"
    
    st.success("Bienvenido!")
    show_pages([
              Page("inicio.py", "Inicio" ),
              Page("completo.py", "Cargar Movimientos"),
              Page("faltante.py", "Parametros de Productos"),
              Page("tablero.py", "Tablero de Stock"),
              Page("consulta.py", "Consulta de Movimientos"),
              

          ])
    
# Create the login form

if st.session_state.ingreso == "ok":
  st.title("Salir del Sistema")
  if st.button("salir"):

    del st.session_state.ingreso
    st.info("Salio Exitosamente del Sistema")
else:
  st.header("Ingrese")
  placeholder = st.empty()
  with placeholder.form("Login"):
      
      username = st.text_input("Usuario")
      password = st.text_input("Password", type="password")
      ingresar = st.form_submit_button("Ingresar")
  if ingresar:
    
      # Check if the username and password are valid
    c.execute("SELECT * FROM Usuarios WHERE Usuarios = ? AND Password = ?", (username, password))

    user = c.fetchone()

      # If the username and password are valid, log the user in
    if user is not None:
          
        login()
          
          
        placeholder.empty()
        # Otherwise, show an error message
    else:
        st.error("Usuario o Contraseña Incorrecta")

        # Add a submit button
local_css("estilos.css")      
