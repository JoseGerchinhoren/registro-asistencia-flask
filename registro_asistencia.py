from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""

    if request.method == "POST":
        dni = request.form["dni"]
        if dni:
            # Aquí puedes agregar la lógica para verificar el DNI en la base de datos
            # y registrar la asistencia
            # Por ahora, simplemente mostraremos un mensaje de confirmación.
            mensaje = f"Asistencia registrada para DNI {dni}"

    return render_template("index.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
