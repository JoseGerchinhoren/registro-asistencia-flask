from flask import Flask, render_template, request, jsonify
import pyodbc
from datetime import datetime
import json
import logging

app = Flask(__name__)

# Configuración de registro
logging.basicConfig(filename='app.log', level=logging.DEBUG)

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
                sql = "SELECT idCliente FROM Cliente WHERE dni = ?"
                cursor.execute(sql, dni)
                id_cliente = cursor.fetchone()

                if id_cliente:
                    sql_insert = "INSERT INTO Asistencia (idCliente, fecha, hora, dni) VALUES (?, ?, ?, ?)"
                    cursor.execute(sql_insert, id_cliente[0], datetime.now().date(), datetime.now().time(), dni)
                    conn.commit()
                    mensaje = f"Asistencia registrada para DNI {dni}"
                    mostrar_mensaje = True
                else:
                    mensaje = "Cliente no encontrado."

                cursor.close()
            except Exception as e:
                mensaje = f"Error al registrar la asistencia: {str(e)}"
                logging.error(f"Error al registrar asistencia: {str(e)}")

    return render_template("index.html", mensaje=mensaje, mostrar_mensaje=mostrar_mensaje)

# Ruta para obtener información del cliente por AJAX
@app.route("/cliente_info/<dni>")
def cliente_info(dni):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nombreApellido FROM Cliente WHERE dni = ?", dni)
        cliente = cursor.fetchone()
        cursor.close()
        if cliente:
            cliente_info = {'nombreApellido': cliente.nombreApellido}
            return jsonify(cliente=cliente_info)
        else:
            return jsonify(error="Cliente no encontrado")
    except Exception as e:
        logging.error(f"Error al obtener información del cliente: {str(e)}")
        return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
