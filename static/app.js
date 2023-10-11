function mostrarMensajeEmergente(mensaje) {
    var mensajeEmergente = document.getElementById('mensaje-emergente');
    mensajeEmergente.textContent = mensaje;
    mensajeEmergente.style.display = 'block';

    // Ocultar el mensaje después de 5 segundos
    setTimeout(function() {
        mensajeEmergente.style.display = 'none';
    }, 5000); // 5 segundos en milisegundos
}

document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector("form");
    var dniInput = document.getElementById("dni");

    form.addEventListener("submit", function(event) {
        event.preventDefault();  // Evita que se envíe el formulario de forma predeterminada

        // Realiza aquí la lógica para mostrar el mensaje emergente con la información del cliente
        mostrarMensajeEmergente("Información del cliente: ...");  // Reemplaza con la información real del cliente

        // Borra el contenido del campo de DNI inmediatamente
        dniInput.value = "";

        // Coloca automáticamente el cursor en el campo de DNI inmediatamente
        dniInput.focus();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var dniInput = document.getElementById("dni");
    dniInput.focus();
});
