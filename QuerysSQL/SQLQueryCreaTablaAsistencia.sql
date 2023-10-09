CREATE TABLE Asistencia (
    idAsistencia INT PRIMARY KEY IDENTITY(1,1),
    idCliente INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    dni VARCHAR(8) NOT NULL
);