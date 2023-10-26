from flask import Flask, render_template, request, jsonify
import pyodbc
from datetime import datetime, timedelta
import json
import logging
from dateutil.relativedelta import relativedelta

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

# Función para calcular el estado de la cuota
def calcular_estado_cuota(ultima_fecha_pago, fecha_actual):
    if ultima_fecha_pago:
        # Obtener la fecha de hoy como datetime.date si es un objeto datetime.datetime
        if isinstance(fecha_actual, datetime):
            fecha_actual = fecha_actual.date()

        # Calcular la fecha de vencimiento (1 mes después de la última fecha de pago)
        fecha_vencimiento = ultima_fecha_pago + relativedelta(months=1)

        if fecha_actual < fecha_vencimiento:
            estado_texto = "Cuota al día"
            estado_color = "green"
        elif fecha_actual == fecha_vencimiento:
            estado_texto = "Vence hoy"
            estado_color = "yellow"
        else:
            estado_texto = "Cuota vencida"
            estado_color = "red"
    else:
        estado_texto = "Sin pagos registrados"
        estado_color = "gray"

    return estado_texto, estado_color

# Ruta para obtener información del cliente por AJAX
@app.route("/cliente_info/<dni>")
def cliente_info(dni):
    try:
        cursor = conn.cursor()
        # Consulta para obtener el último pago del cliente
        cursor.execute("""
            SELECT C.nombreApellido, MAX(P.fechaPago) as ultima_fecha_pago
            FROM Cliente C
            LEFT JOIN Pago P ON C.idCliente = P.idCliente
            WHERE C.dni = ?
            GROUP BY C.nombreApellido
        """, dni)

        cliente_info = cursor.fetchone()

        if cliente_info:
            # Accede a las columnas por índice
            nombre = cliente_info[0]
            ultima_fecha_pago = cliente_info[1]
            estado_texto, estado_color = calcular_estado_cuota(ultima_fecha_pago, datetime.now().date())

            return jsonify(cliente={
                'nombreApellido': nombre,
                'estado_cuota': estado_texto,
                'color_cuota': estado_color
            })
        else:
            return jsonify(error="Cliente no encontrado")
    except Exception as e:
        logging.error(f"Error al obtener información del cliente: {str(e)}")
        return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(debug=True)