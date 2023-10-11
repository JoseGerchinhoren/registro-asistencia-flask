from flask import Flask, render_template, request, jsonify
import pyodbc
from datetime import datetime
import json

app = Flask(__name__)

# Configuración de la conexión a la base de datos SixGym
# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Conexión a la base de datos SQL Server
conn = pyodbc.connect(
    driver=config["driver"],
    server=config["server"],
    database=config["database"],
    uid=config["user"],
    pwd=config["password"]
)

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    mostrar_mensaje = False

    if request.method == "POST":
        dni = request.form["dni"]
        if dni and len(dni) == 8:  # Verifica que el DNI tenga 8 dígitos
            try:
                cursor = conn.cursor()

                # Agrega la lógica para verificar el DNI en la base de datos (puede variar según tu esquema de base de datos)
                # Supongamos que tienes una tabla "clientes" con una columna "dni" y una columna "idCliente"
                cursor.execute("SELECT idCliente FROM Cliente WHERE dni = ?", dni)
                id_cliente = cursor.fetchone()

                if id_cliente:
                    # Registra la asistencia en la tabla "asistencia"
                    cursor.execute("INSERT INTO Asistencia (idCliente, fecha, hora, dni) VALUES (?, ?, ?, ?)",
                                   id_cliente[0], datetime.now().date(), datetime.now().time(), dni)
                    conn.commit()
                    mensaje = f"Asistencia registrada para DNI {dni}"
                    mostrar_mensaje = True
                    informacion_del_cliente = "Cliente"
                    mensaje_emergente = f"Información del cliente: {informacion_del_cliente}"  # Reemplaza con la información real del cliente
                    mensaje_html = f"{mensaje}<br><div id='mensaje-emergente' class='mensaje-emergente'>{mensaje_emergente}</div>"
                    script = f"<script>mostrarMensajeEmergente('{mensaje_emergente}');</script>"
                    return render_template("index.html", mensaje=mensaje_html, mostrar_mensaje=mostrar_mensaje, mensaje_emergente=mensaje_emergente, script=script)
                else:
                    mensaje = "Cliente no encontrado."

                cursor.close()
            except Exception as e:
                mensaje = f"Error al registrar la asistencia: {str(e)}"

    return render_template("index.html", mensaje=mensaje, mostrar_mensaje=mostrar_mensaje)

# Ruta para obtener información del cliente por AJAX
@app.route("/cliente_info/<dni>")
def cliente_info(dni):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE dni = ?", dni)
        cliente = cursor.fetchone()
        cursor.close()
        if cliente:
            return jsonify(cliente=cliente)
        else:
            return jsonify(error="Cliente no encontrado")
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
