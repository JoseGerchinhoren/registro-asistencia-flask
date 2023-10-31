document.addEventListener("DOMContentLoaded", function () {
    // Agrega un evento para el formulario de asistencia
    const asistenciaForm = document.getElementById("asistencia-form");
    const dniInput = document.getElementById("dni");

    asistenciaForm.addEventListener("submit", function (e) {
        e.preventDefault(); // Evita el envío normal del formulario

        // Obtiene el valor del DNI
        const dni = dniInput.value;

        // Limpia el campo DNI inmediatamente
        dniInput.value = "";

        // Realiza una solicitud AJAX para obtener la información del cliente
        fetch(`/cliente_info/${dni}`)
            .then(response => response.json())
            .then(data => {
                if (data.cliente) {
                    const cliente = data.cliente;
                    const mensajeEmergente = document.getElementById("mensaje-emergente");
                    mensajeEmergente.innerHTML = `
                        <p>Información del Cliente:</p>
                        <p>Nombre: ${cliente.nombreApellido}</p>
                        <p>Estado de la Cuota: ${cliente.estado_cuota}</p>`;
                    mensajeEmergente.style.display = "block";

                    // Reproduce el sonido basado en el estado de la cuota
                    if (cliente.color_cuota === "green") {
                        // Cliente con cuota al día
                        new Audio("/sounds/positive.mp3").play();
                    } else {
                        // Cliente con cuota vencida o sin pagos registrados
                        new Audio("/sounds/negative.mp3").play();
                    }

                    // Oculta el mensaje emergente después de 10 segundos
                    setTimeout(() => {
                        mensajeEmergente.style.display = "none";
                        dniInput.focus(); // Enfoca el campo DNI
                    }, 5000);
                } else {
                    alert("Cliente no encontrado.");
                }
            })
            .catch(error => {
                console.error("Error en la solicitud AJAX:", error);
            });
    });
});
