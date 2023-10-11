
# import streamlit as st
# import sqlite3
# from st_pages import Page, show_pages, add_page_title
# import base64
# from mail import enviarmail

# # Connect to the SQLite database
# conn = sqlite3.connect("inventario.db")
# LOGO_IMAGE = "./imagenes/tatito.jpeg"
# # Create a cursor
# c = conn.cursor()

# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#                      .container {
#                 display: flex;
#             }
#             .logo-text {
#                 font-weight:700 !important;
#                 font-size:30px !important;
#                 color: black !important;
#                 padding-top: 50px !important;
#             }
#             .logo-img {
#                 float:right;
#             }
#             </style>
#             """
# st.markdown(hide_st_style, 

#     unsafe_allow_html=True)
# st.title("Movimiento de Inventario")
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)   
# st.markdown(
   

    
#     f"""
#     <div class="container">
#         <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" > <br>
        
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# if "ingreso" not in st.session_state:
#       st.session_state.ingreso = ""

# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# def login(user):
#     st.session_state.ingreso = "ok"
#     if user[2] == 1:  # Si el nivel del usuario es 1

#         enviarmail()
#         st.success("Bienvenido!")
#         show_pages([
#                   Page("inicio.py", "Inicio" ),
#                   Page("completo.py", "Cargar Movimientos"),
#                   Page("faltante.py", "Carga Aviso Faltante"),
#                   Page("actmanual.py", "Correccion de Stock"),
#                   Page("tablero.py", "Tablero de Stock"),
#                   Page("consulta.py", "Consulta de Movimientos"),
#                   Page("actualizarmedidas.py", "Actualizar Productos"),
#               ])
#     else:
#         st.success("Bienvenido!")
#         show_pages([
#                   Page("inicio.py", "Inicio" ),
#                   Page("completo.py", "Cargar Movimientos"),
#                   Page("faltante.py", "Carga Aviso Faltante"),
#                   Page("actmanual.py", "Correccion de Stock"),
#                   Page("actualizarmedidas.py", "Carga Parametros Cantidad Productos"),
#               ])



# # Create the login form

# if st.session_state.ingreso == "ok":
#   st.title("Salir del Sistema")
#   if st.button("salir"):

#     del st.session_state.ingreso
#     st.info("Salio Exitosamente del Sistema")
# else:
#   st.header("Ingrese")
#   placeholder = st.empty()
#   with placeholder.form("Login"):
      
#       username = st.text_input("Usuario")
#       password = st.text_input("Password", type="password")
#       ingresar = st.form_submit_button("Ingresar")
#   if ingresar:
    
#       # Check if the username and password are valid
#     c.execute("SELECT * FROM Usuarios WHERE Usuarios = ? AND Password = ?", (username, password))

#     user = c.fetchone()

#       # If the username and password are valid, log the user in
#     if user is not None:
          
#         login(user)
          
          
#         placeholder.empty()
#         # Otherwise, show an error message
#     else:
#         st.error("Usuario o Contraseña Incorrecta")

#         # Add a submit button
# local_css("estilos.css")
import streamlit as st
import sqlite3
from st_pages import Page, show_pages, add_page_title
import base64
from mail import enviarmail

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
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title("Movimiento de Inventario")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" > <br>
    </div>
    """,
    unsafe_allow_html=True
)

if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""
# if "username" not in st.session_state:
#     st.session_state.username = ""
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def login(user):
    st.session_state.ingreso = "ok"
    # st.write(st.session_state.user)
    if user[2] == 1:  # Si el nivel del usuario es 1
        enviarmail()
        st.success("Bienvenido!")
        show_pages([
            Page("inicio.py", "Inicio" ),
            Page("completo.py", "Cargar Movimientos"),
            Page("faltante.py", "Carga Aviso Faltante"),
            Page("actmanual.py", "Correccion de Stock"),
            Page("tablero.py", "Tablero de Stock"),
            Page("consulta.py", "Consulta de Movimientos"),
            Page("actualizarmedidas.py", "Actualizar Productos"),
            Page("actualizarprecios.py", "Actualizar Precios"),
        ])
    else:
        st.success("Bienvenido!")
        show_pages([
            Page("inicio.py", "Inicio" ),
            Page("completo.py", "Cargar Movimientos"),
            Page("faltante.py", "Carga Aviso Faltante"),
            Page("actmanual.py", "Correccion de Stock"),
            Page("actualizarmedidas.py", "Carga Parametros Cantidad Productos"),
            Page("actualizarprecios.py", "Actualizar Precios"),
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
        username = st.text_input("Usuario")  # Agregar key para identificar el campo
        password = st.text_input("Password", type="password")
        ingresar = st.form_submit_button("Ingresar")
    if ingresar:
        # Check if the username and password are valid
        c.execute("SELECT * FROM Usuarios WHERE Usuarios = ? AND Password = ?", (username, password))
        user = c.fetchone()
        # If the username and password are valid, log the user in
        if user is not None:
            
            # st.session_state.user = username

            login(user)
            placeholder.empty()
        # Otherwise, show an error message
        else:
            st.error("Usuario o Contraseña Incorrecta")

# Add a submit button
local_css("estilos.css")
