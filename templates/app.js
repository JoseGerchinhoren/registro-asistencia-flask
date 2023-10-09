document.addEventListener("DOMContentLoaded", function () {
    // Agrega un evento para el formulario de asistencia
    document.getElementById("asistencia-form").addEventListener("submit", function (e) {
        e.preventDefault(); // Evita el envío normal del formulario

        // Realiza una solicitud AJAX para obtener la información del cliente
        const dni = document.getElementById("dni").value;
        fetch(`/cliente_info/${dni}`)
            .then(response => response.json())
            .then(data => {
                if (data.cliente) {
                    const cliente = data.cliente;
                    const mensajeEmergente = document.getElementById("mensaje-emergente");
                    mensajeEmergente.innerHTML = `
                        <p>Información del Cliente:</p>
                        <p>Nombre: ${cliente.nombre}</p>
                        <p>Estado de la Cuota: ${cliente.estado_cuota}</p>
                        <p>Días en el Mes: ${cliente.dias_en_el_mes}</p>
                    `;
                    mensajeEmergente.style.display = "block";

                    // Oculta el mensaje emergente después de 10 segundos
                    setTimeout(() => {
                        mensajeEmergente.style.display = "none";
                        document.getElementById("dni").value = ""; // Limpia el campo DNI
                    }, 10000);
                } else {
                    alert("Cliente no encontrado.");
                }
            })
            .catch(error => {
                console.error(error);
            });
    });
});
