-- Crear la base de datos
CREATE DATABASE Proyecto1;
USE Proyecto1;

-- Tabla para los estados permitidos de la propiedad
CREATE TABLE EstadosPermitidos (
    idEstado INT PRIMARY KEY,
    estado VARCHAR(20)
);

-- Insertar valores permitidos en EstadosPermitidos
INSERT INTO EstadosPermitidos (idEstado, estado) VALUES
(1, 'disponible'),
(2, 'ocupado'),
(3, 'en mantenimiento');

-- Tabla para los tipos de pago permitidos
CREATE TABLE TiposPagoPermitidos (
    idTipoPago INT PRIMARY KEY,
    tipoPago VARCHAR(20)
);

-- Insertar valores permitidos en TiposPagoPermitidos
INSERT INTO TiposPagoPermitidos (idTipoPago, tipoPago) VALUES
(1, 'alquiler'),
(2, 'servicios'),
(3, 'mantenimiento');


-- Tabla para los estados de pago permitidos
CREATE TABLE EstadosPagoPermitidos (
    idEstadoPago INT PRIMARY KEY,
    estadoPago VARCHAR(20)
);

-- Insertar valores permitidos en EstadosPagoPermitidos
INSERT INTO EstadosPagoPermitidos (idEstadoPago, estadoPago) VALUES
(1, 'pendiente'),
(2, 'realizado'),
(3, 'atrasado');

-- Tabla para los estados de mantenimiento permitidos
CREATE TABLE EstadosMantenimientoPermitidos (
    idEstadoMantenimiento INT PRIMARY KEY,
    estadoMantenimiento VARCHAR(20)
);

-- Insertar valores permitidos en EstadosMantenimientoPermitidos
INSERT INTO EstadosMantenimientoPermitidos (idEstadoMantenimiento, estadoMantenimiento) VALUES
(1, 'pendiente'),
(2, 'en proceso'),
(3, 'resuelto');

-- Tabla para las prioridades permitidas
CREATE TABLE PrioridadesPermitidas (
    idPrioridad INT PRIMARY KEY,
    prioridad VARCHAR(20)
);

-- Insertar valores permitidos en PrioridadesPermitidas
INSERT INTO PrioridadesPermitidas (idPrioridad, prioridad) VALUES
(1, 'baja'),
(2, 'media'),
(3, 'alta');

-- Tabla para la entidad Usuario
CREATE TABLE Usuario (
    cedula INT PRIMARY KEY,
    nombre VARCHAR(20),
    apellido1 VARCHAR(20),
    apellido2 VARCHAR(20),
    telefono INT,
    correo VARCHAR(100)
);

-- Tabla para la entidad Propietario
CREATE TABLE Propietario (
    cedula INT PRIMARY KEY,
    FOREIGN KEY (cedula) REFERENCES Usuario(cedula)
);

-- Tabla para la entidad Inquilino
CREATE TABLE Inquilino (
    cedula INT PRIMARY KEY,
    FOREIGN KEY (cedula) REFERENCES Usuario(cedula)
);

-- Tabla para la entidad Propiedad
CREATE TABLE Propiedad (
    idPropiedad INT PRIMARY KEY,
    direccion VARCHAR(90),
    tipoPropiedad VARCHAR(12),
    numeroHabitaciones INT,
    tamanoMetros INT,
    descripcion VARCHAR(90),
    estadoActual INT,
    precioAlquiler INT,
    gastosAdicionales INT,
    cedulaPropietario INT,
    FOREIGN KEY (estadoActual) REFERENCES EstadosPermitidos(idEstado),
    FOREIGN KEY (cedulaPropietario) REFERENCES Propietario(cedula)
);

-- Tabla para la entidad Documento
CREATE TABLE Documento (
    cedulaInquilino INT, 
    tipo VARCHAR(10),
    archivo VARBINARY(MAX),
    FOREIGN KEY (cedulaInquilino) REFERENCES Inquilino(cedula)
);

-- Tabla para la entidad Alquiler
CREATE TABLE Alquiler (
    cedulaInquilino INT,
    idPropiedad INT,
    fechaInicio DATE,
    fechaFin DATE,
    FOREIGN KEY (cedulaInquilino) REFERENCES Inquilino(cedula),
    FOREIGN KEY (idPropiedad) REFERENCES Propiedad(idPropiedad)
);

-- Tabla para la entidad Pagos
CREATE TABLE Pagos (
    idPago INT PRIMARY KEY,
    cedulaInquilino INT, 
    fechaPago DATE,
    monto INT,
    tipoPago INT,
    estadoPago INT, 
    metodoPago VARCHAR(20),
    FOREIGN KEY (cedulaInquilino) REFERENCES Inquilino(cedula),
    FOREIGN KEY (tipoPago) REFERENCES TiposPagoPermitidos(idTipoPago),
    FOREIGN KEY (estadoPago) REFERENCES EstadosPagoPermitidos(idEstadoPago) 
);

-- Tabla para la entidad Proveedores
CREATE TABLE Proveedores (
    idProveedor INT PRIMARY KEY,
    nombre VARCHAR(20),
    primerApellido VARCHAR(20),
    segundoApellido VARCHAR(20),
    especialidad VARCHAR(60),
    correo VARCHAR(100),
    telefono INT
);

INSERT INTO Proveedores (idProveedor, nombre, primerApellido, segundoApellido, correo, telefono, especialidad) VALUES
(1, 'Juan', 'Perez', 'Garcia', 'juanperez@example.com', 123456789, 'Electricista'),
(2, 'Maria', 'Gomez', 'Lopez', 'mariagomez@example.com', 987654321, 'Jardinero'),
(3, 'Carlos', 'Martinez', 'Fernandez', 'carlosmartinez@example.com', 555666777, 'Carpintero'),
(4, 'Ana', 'Ruiz', 'Sanchez', 'anaruiz@example.com', 111222333, 'Plomero'),
(5, 'Pedro', 'Diaz', 'Gutierrez', 'pedrodiaz@example.com', 444555666, 'Pintor');

-- Tabla para la entidad Solicitud de Mantenimiento
CREATE TABLE SolicitudMantenimiento (
    idSolicitud INT PRIMARY KEY,
    idPropiedad INT,
    descripcionProblema VARCHAR(100),
    idProveedor INT,
    fechaSolicitud DATE,
    estado INT,
    idPrioridad INT,
    FOREIGN KEY (idPropiedad) REFERENCES Propiedad(idPropiedad),
    FOREIGN KEY (idProveedor) REFERENCES Proveedores(idProveedor),
    FOREIGN KEY (estado) REFERENCES EstadosMantenimientoPermitidos(idEstadoMantenimiento),
    FOREIGN KEY (idPrioridad) REFERENCES PrioridadesPermitidas(idPrioridad)
);

-- Tabla para la entidad FotoPropiedad
CREATE TABLE FotoPropiedad (
    idPropiedad INT,
    tipo VARCHAR(10),
    archivo VARBINARY(MAX),
    FOREIGN KEY (idPropiedad) REFERENCES Propiedad(idPropiedad)
);

-- Tabla para la entidad Comunicacion
CREATE TABLE Comunicacion (
    cedulaEmisor INT,
    cedulaReceptor INT,
    fechaMensaje DATE,
    horaMensaje TIME,
    contenido VARCHAR(100),
    estado VARCHAR(20),
    FOREIGN KEY (cedulaEmisor) REFERENCES Usuario(cedula),
    FOREIGN KEY (cedulaReceptor) REFERENCES Usuario(cedula) 
);

-- Tabla para la entidad Trabajos
CREATE TABLE Trabajos (
    idProveedor INT,
    idTrabajo VARCHAR(20) PRIMARY KEY,
    idSolicitud INT, 
    descripcion VARCHAR(300),
    FOREIGN KEY (idProveedor) REFERENCES Proveedores(idProveedor),
    FOREIGN KEY (idSolicitud) REFERENCES SolicitudMantenimiento(idSolicitud) 
);

-- Tabla para la entidad FotosProblema
CREATE TABLE FotosProblema (
    idSolicitud INT,
    foto VARBINARY(MAX),
    FOREIGN KEY (idSolicitud) REFERENCES SolicitudMantenimiento(idSolicitud)
);

-- Tabla para la entidad ComentariosInquilino
CREATE TABLE ComentariosInquilino (
    idComentario INT PRIMARY KEY,
    comentario VARCHAR(300),
    idSolicitud INT, 
    FOREIGN KEY (idSolicitud) REFERENCES SolicitudMantenimiento(idSolicitud) 
);