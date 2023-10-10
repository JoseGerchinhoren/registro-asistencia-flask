function mostrarMensajeEmergente(mensaje) {
    var mensajeEmergente = document.getElementById('mensaje-emergente');
    mensajeEmergente.textContent = mensaje;
    mensajeEmergente.style.display = 'block';

    // Ocultar el mensaje después de 10 segundos
    setTimeout(function() {
        mensajeEmergente.style.display = 'none';
    }, 5000); // 10 segundos en milisegundos
}