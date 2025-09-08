CREATE DATABASE Hotel;
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
	tipo_usuario VARCHAR(20),
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    clave VARCHAR(10) NOT NULL,
	id_usuario_crea INT NULL,
    id_usuario_edita INT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_edicion DATETIME NULL
);

CREATE TABLE Administrador (
    id_administrador INT PRIMARY KEY,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Cliente (
    id_cliente INT PRIMARY KEY,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Tipo_Habitacion (
    id_tipo INT PRIMARY KEY IDENTITY(100,1),
    nombre_tipo VARCHAR(50) NOT NULL,
    descripcion TEXT,
    id_usuario_crea INT NULL,
    id_usuario_edita INT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_edicion DATETIME NULL
);

CREATE TABLE Habitacion (
    id_habitacion INT PRIMARY KEY IDENTITY(100,1),
    numero VARCHAR(10) NOT NULL,
    id_tipo INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    disponible BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_tipo) REFERENCES Tipo_Habitacion(id_tipo),
    id_usuario_crea INT NULL,
    id_usuario_edita INT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_edicion DATETIME NULL
);

CREATE TABLE Reserva (
    id_reserva INT PRIMARY KEY IDENTITY(100,1),
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    estado_reserva VARCHAR(50) NOT NULL,
    numero_de_personas INT NOT NULL,
    noches INT NOT NULL,
    costo_total FLOAT(20) NOT NULL,
    id_cliente INT NOT NULL,
    id_habitacion INT NOT NULL,
    id_usuario_crea INT NULL,
    id_usuario_edita INT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_edicion DATETIME NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_habitacion) REFERENCES Habitacion(id_habitacion)
);

CREATE TABLE Servicios_Adicionales (
    id_servicio INT PRIMARY KEY IDENTITY(100,1),
    nombre_servicio VARCHAR(100) NOT NULL,
    precio FLOAT(30) NOT NULL,
    id_usuario_crea INT NULL,
    id_usuario_edita INT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_edicion DATETIME NULL
);

CREATE TABLE Reserva_Servicios (
    id_reserva INT NOT NULL,
    id_servicio INT NOT NULL,
    id_usuario_crea INT NULL,
    id_usuario_edita INT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_edicion DATETIME NULL,
    PRIMARY KEY (id_reserva, id_servicio),
    FOREIGN KEY (id_reserva) REFERENCES Reserva(id_reserva),
    FOREIGN KEY (id_servicio) REFERENCES Servicios_Adicionales(id_servicio)
);