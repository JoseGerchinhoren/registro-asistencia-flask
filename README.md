# Registro de Asistencia para SixGym

Este es un proyecto de registro de asistencia desarrollado para el gimnasio SixGym. La aplicación permite a los clientes del gimnasio registrar su asistencia de manera rápida y sencilla.

## Desarrollo

Este proyecto se ha desarrollado con entusiasmo, aprendizaje y dedicación. Aquí tienes un resumen de cómo se construyó:

1. **Elección de Tecnologías**: Decidí utilizar Flask, un marco de desarrollo web en Python, para construir la aplicación. Tenía conocimientos básicos de HTML, CSS y JavaScript, y este proyecto me brindó la oportunidad de poner esos conocimientos en práctica.

2. **Desafíos y Aprendizaje**: Al ser uno de mis primeros proyectos con estas tecnologías, enfrenté varios desafíos. Aprendí a trabajar con Flask, crear formularios HTML, realizar solicitudes AJAX con JavaScript y conectar con una base de datos SQL Server.

3. **Asistencia de ChatGPT**: En el proceso de desarrollo, ChatGPT se convirtió en mi guía para resolver problemas y aprender nuevas tecnologías. Sus sugerencias y ejemplos fueron invaluables para superar obstáculos.

## Funcionamiento

La aplicación es simple y eficaz:

1. Los clientes ingresan su número de identificación personal (DNI) en el campo correspondiente.
2. Al presionar "Enter", la aplicación verifica la base de datos para validar el DNI.
3. Si el DNI es válido, se registra la asistencia del cliente.
4. Se muestra un mensaje emergente con información del cliente durante 5 segundos.
5. El campo del DNI se limpia automáticamente, y el cursor se mantiene en el campo para facilitar el registro de otros clientes.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalado Python y las siguientes bibliotecas:

- Flask
- pyodbc

Puedes instalar estas bibliotecas utilizando pip:

```bash
pip install flask pyodbc
```

## Configuracion

Para configurar la conexión a la base de datos SQL Server, crea un archivo config.json en el directorio raíz del proyecto con la siguiente estructura:

```bash
{
  "driver": "DriverName",
  "server": "ServerName",
  "database": "DatabaseName",
  "user": "YourUsername",
  "password": "YourPassword"
}

```

## Ejecución
Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
python app.py
```

La aplicación estará disponible en http://localhost:5000/ en tu navegador web.