
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
def enviarmail():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor
    c = conn.cursor()

    # Obtener la dirección de correo electrónico de la tabla 'mail'
    c.execute("SELECT mail FROM mail")
    email_address = c.fetchone()[0]

    # Obtener los datos de las tablas 'Inventario' y 'Productos' donde 'Cantidad_Stock' es menor que 'Faltante'
    c.execute("SELECT p.Nombre, i.Cantidad_Stock, i.Faltante FROM Inventario i INNER JOIN Productos p ON i.Codigo = p.Codigo WHERE i.Cantidad_Stock < i.Faltante")
    data = c.fetchall()

    # Preparar el correo electrónico
    msg = MIMEMultipart()
    msg['From'] = "tatitocorrientes@gmail.com"
    msg['To'] = email_address
    msg['Subject'] = "Inventario con stock bajo"

    body = "<html><body><p>Los siguientes elementos tienen un stock bajo:</p>"
    body += "<table border='1'><tr><th>Nombre</th><th>Cantidad_Stock</th><th>Faltante</th></tr>"
    for row in data:
        body += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    body += "</table></body></html>"

    msg.attach(MIMEText(body, 'html'))

    # Configurar el servidor SMTP (aquí usando gmail)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Ingresar las credenciales de correo electrónico
    email_password = "afpcvfpqsyutsqky"
    server.login("tatitocorrientes@gmail.com", email_password)

    # Enviar el correo electrónico
    text = msg.as_string()
    server.sendmail("tatitocorrientes@gmail.com", email_address, text)
    server.quit()
