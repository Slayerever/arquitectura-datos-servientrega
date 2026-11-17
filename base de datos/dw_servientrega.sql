-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-11-2026 a las 00:00:56
-- Versión del servidor: 10.11.16-MariaDB
-- Versión de PHP: 8.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dw_servientrega`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dim_cliente`
--

CREATE TABLE `dim_cliente` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `tipo_cliente` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dim_cliente`
--

INSERT INTO `dim_cliente` (`id_cliente`, `nombre`, `tipo_cliente`) VALUES
(1, 'Comercial Andina S.A.S.', 'Empresa'),
(2, 'Distribuciones Central S.A.S.', 'Empresa'),
(3, 'Carlos Ramirez', 'Persona natural');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dim_estado`
--

CREATE TABLE `dim_estado` (
  `id_estado` int(11) NOT NULL,
  `estado_envio` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dim_estado`
--

INSERT INTO `dim_estado` (`id_estado`, `estado_envio`) VALUES
(1, 'Entregado'),
(2, 'En transito'),
(3, 'Pendiente'),
(4, 'Devuelto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dim_servicio`
--

CREATE TABLE `dim_servicio` (
  `id_servicio` int(11) NOT NULL,
  `tipo_servicio` varchar(100) DEFAULT NULL,
  `descripcion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dim_servicio`
--

INSERT INTO `dim_servicio` (`id_servicio`, `tipo_servicio`, `descripcion`) VALUES
(1, 'Express', 'Entrega prioritaria'),
(2, 'Estandar', 'Servicio de entrega regular'),
(3, 'Especial', 'Servicio logistico especial');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dim_tiempo`
--

CREATE TABLE `dim_tiempo` (
  `id_tiempo` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `dia` int(11) DEFAULT NULL,
  `mes` int(11) DEFAULT NULL,
  `anio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dim_tiempo`
--

INSERT INTO `dim_tiempo` (`id_tiempo`, `fecha`, `dia`, `mes`, `anio`) VALUES
(1, '2025-11-01', 1, 11, 2025),
(2, '2025-11-02', 2, 11, 2025),
(3, '2025-11-03', 3, 11, 2025),
(4, '2025-11-04', 4, 11, 2025),
(5, '2025-11-05', 5, 11, 2025);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dim_ubicacion`
--

CREATE TABLE `dim_ubicacion` (
  `id_ubicacion` int(11) NOT NULL,
  `ciudad_origen` varchar(100) DEFAULT NULL,
  `departamento_origen` varchar(100) DEFAULT NULL,
  `ciudad_destino` varchar(100) DEFAULT NULL,
  `departamento_destino` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dim_ubicacion`
--

INSERT INTO `dim_ubicacion` (`id_ubicacion`, `ciudad_origen`, `departamento_origen`, `ciudad_destino`, `departamento_destino`) VALUES
(1, 'Bogota', 'Cundinamarca', 'Medellin', 'Antioquia'),
(2, 'Medellin', 'Antioquia', 'Bogota', 'Cundinamarca'),
(3, 'Cali', 'Valle del Cauca', 'Bogota', 'Cundinamarca'),
(4, 'Barranquilla', 'Atlantico', 'Cartagena', 'Bolivar');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `envios_reconstruidos`
--

CREATE TABLE `envios_reconstruidos` (
  `id_envio` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_tiempo` int(11) DEFAULT NULL,
  `id_ubicacion` int(11) DEFAULT NULL,
  `id_servicio` int(11) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `fecha_prometida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `tiempo_entrega_horas` decimal(8,2) DEFAULT NULL,
  `cantidad_paquetes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `envios_reconstruidos`
--

INSERT INTO `envios_reconstruidos` (`id_envio`, `id_cliente`, `id_tiempo`, `id_ubicacion`, `id_servicio`, `id_estado`, `fecha_prometida`, `fecha_entrega`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1001, 1, 1, 1, 1, 1, '2025-11-03', '2025-11-02', 24.00, 1),
(1002, 2, 2, 2, 2, 1, '2025-11-05', '2025-11-05', 72.00, 2),
(1005, 2, 5, 1, 3, 4, '2025-11-09', '2025-11-10', 120.00, 1),
(1003, 3, 3, 3, 1, 1, '2025-11-06', '2025-11-04', 30.00, 1),
(1004, 1, 4, 4, 2, 2, '2025-11-08', NULL, NULL, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fragmento_nodo1`
--

CREATE TABLE `fragmento_nodo1` (
  `id_envio` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tiempo` int(11) NOT NULL,
  `id_ubicacion` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_estado` int(11) NOT NULL,
  `fecha_prometida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `tiempo_entrega_horas` decimal(8,2) DEFAULT NULL,
  `cantidad_paquetes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fragmento_nodo1`
--

INSERT INTO `fragmento_nodo1` (`id_envio`, `id_cliente`, `id_tiempo`, `id_ubicacion`, `id_servicio`, `id_estado`, `fecha_prometida`, `fecha_entrega`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1001, 1, 1, 1, 1, 1, '2025-11-03', '2025-11-02', 24.00, 1),
(1002, 2, 2, 2, 2, 1, '2025-11-05', '2025-11-05', 72.00, 2),
(1005, 2, 5, 1, 3, 4, '2025-11-09', '2025-11-10', 120.00, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fragmento_nodo2`
--

CREATE TABLE `fragmento_nodo2` (
  `id_envio` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tiempo` int(11) NOT NULL,
  `id_ubicacion` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_estado` int(11) NOT NULL,
  `fecha_prometida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `tiempo_entrega_horas` decimal(8,2) DEFAULT NULL,
  `cantidad_paquetes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fragmento_nodo2`
--

INSERT INTO `fragmento_nodo2` (`id_envio`, `id_cliente`, `id_tiempo`, `id_ubicacion`, `id_servicio`, `id_estado`, `fecha_prometida`, `fecha_entrega`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1003, 3, 3, 3, 1, 1, '2025-11-06', '2025-11-04', 30.00, 1),
(1004, 1, 4, 4, 2, 2, '2025-11-08', NULL, NULL, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fragmento_nodo2_recon`
--

CREATE TABLE `fragmento_nodo2_recon` (
  `id_envio` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_tiempo` int(11) DEFAULT NULL,
  `id_ubicacion` int(11) DEFAULT NULL,
  `id_servicio` int(11) DEFAULT NULL,
  `id_estado` int(11) DEFAULT NULL,
  `fecha_prometida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `tiempo_entrega_horas` decimal(8,2) DEFAULT NULL,
  `cantidad_paquetes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fragmento_nodo2_recon`
--

INSERT INTO `fragmento_nodo2_recon` (`id_envio`, `id_cliente`, `id_tiempo`, `id_ubicacion`, `id_servicio`, `id_estado`, `fecha_prometida`, `fecha_entrega`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1003, 3, 3, 3, 1, 1, '2025-11-06', '2025-11-04', 30.00, 1),
(1004, 1, 4, 4, 2, 2, '2025-11-08', NULL, NULL, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fragmento_vertical_identificacion`
--

CREATE TABLE `fragmento_vertical_identificacion` (
  `id_envio` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tiempo` int(11) NOT NULL,
  `id_ubicacion` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fragmento_vertical_identificacion`
--

INSERT INTO `fragmento_vertical_identificacion` (`id_envio`, `id_cliente`, `id_tiempo`, `id_ubicacion`, `id_servicio`, `id_estado`) VALUES
(1001, 1, 1, 1, 1, 1),
(1002, 2, 2, 2, 2, 1),
(1003, 3, 3, 3, 1, 1),
(1004, 1, 4, 4, 2, 2),
(1005, 2, 5, 1, 3, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fragmento_vertical_medicion`
--

CREATE TABLE `fragmento_vertical_medicion` (
  `id_envio` int(11) NOT NULL,
  `fecha_prometida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `tiempo_entrega_horas` decimal(8,2) DEFAULT NULL,
  `cantidad_paquetes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fragmento_vertical_medicion`
--

INSERT INTO `fragmento_vertical_medicion` (`id_envio`, `fecha_prometida`, `fecha_entrega`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1001, '2025-11-03', '2025-11-02', 24.00, 1),
(1002, '2025-11-05', '2025-11-05', 72.00, 2),
(1003, '2025-11-06', '2025-11-04', 30.00, 1),
(1004, '2025-11-08', NULL, NULL, 3),
(1005, '2025-11-09', '2025-11-10', 120.00, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hechos_envios`
--

CREATE TABLE `hechos_envios` (
  `id_envio` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tiempo` int(11) NOT NULL,
  `id_ubicacion` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_estado` int(11) NOT NULL,
  `fecha_prometida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `tiempo_entrega_horas` decimal(8,2) DEFAULT NULL,
  `cantidad_paquetes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `hechos_envios`
--

INSERT INTO `hechos_envios` (`id_envio`, `id_cliente`, `id_tiempo`, `id_ubicacion`, `id_servicio`, `id_estado`, `fecha_prometida`, `fecha_entrega`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1001, 1, 1, 1, 1, 1, '2025-11-03', '2025-11-02', 24.00, 1),
(1002, 2, 2, 2, 2, 1, '2025-11-05', '2025-11-05', 72.00, 2),
(1003, 3, 3, 3, 1, 1, '2025-11-06', '2025-11-04', 30.00, 1),
(1004, 1, 4, 4, 2, 2, '2025-11-08', NULL, NULL, 3),
(1005, 2, 5, 1, 3, 4, '2025-11-09', '2025-11-10', 120.00, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `dim_cliente`
--
ALTER TABLE `dim_cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `dim_estado`
--
ALTER TABLE `dim_estado`
  ADD PRIMARY KEY (`id_estado`);

--
-- Indices de la tabla `dim_servicio`
--
ALTER TABLE `dim_servicio`
  ADD PRIMARY KEY (`id_servicio`);

--
-- Indices de la tabla `dim_tiempo`
--
ALTER TABLE `dim_tiempo`
  ADD PRIMARY KEY (`id_tiempo`);

--
-- Indices de la tabla `dim_ubicacion`
--
ALTER TABLE `dim_ubicacion`
  ADD PRIMARY KEY (`id_ubicacion`);

--
-- Indices de la tabla `fragmento_nodo1`
--
ALTER TABLE `fragmento_nodo1`
  ADD PRIMARY KEY (`id_envio`),
  ADD KEY `fk_envio_cliente` (`id_cliente`),
  ADD KEY `fk_envio_tiempo` (`id_tiempo`),
  ADD KEY `fk_envio_ubicacion` (`id_ubicacion`),
  ADD KEY `fk_envio_servicio` (`id_servicio`),
  ADD KEY `fk_envio_estado` (`id_estado`);

--
-- Indices de la tabla `fragmento_nodo2`
--
ALTER TABLE `fragmento_nodo2`
  ADD PRIMARY KEY (`id_envio`),
  ADD KEY `fk_envio_cliente` (`id_cliente`),
  ADD KEY `fk_envio_tiempo` (`id_tiempo`),
  ADD KEY `fk_envio_ubicacion` (`id_ubicacion`),
  ADD KEY `fk_envio_servicio` (`id_servicio`),
  ADD KEY `fk_envio_estado` (`id_estado`);

--
-- Indices de la tabla `fragmento_nodo2_recon`
--
ALTER TABLE `fragmento_nodo2_recon`
  ADD PRIMARY KEY (`id_envio`);

--
-- Indices de la tabla `hechos_envios`
--
ALTER TABLE `hechos_envios`
  ADD PRIMARY KEY (`id_envio`),
  ADD KEY `fk_envio_cliente` (`id_cliente`),
  ADD KEY `fk_envio_tiempo` (`id_tiempo`),
  ADD KEY `fk_envio_ubicacion` (`id_ubicacion`),
  ADD KEY `fk_envio_servicio` (`id_servicio`),
  ADD KEY `fk_envio_estado` (`id_estado`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `hechos_envios`
--
ALTER TABLE `hechos_envios`
  ADD CONSTRAINT `fk_envio_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `dim_cliente` (`id_cliente`),
  ADD CONSTRAINT `fk_envio_estado` FOREIGN KEY (`id_estado`) REFERENCES `dim_estado` (`id_estado`),
  ADD CONSTRAINT `fk_envio_servicio` FOREIGN KEY (`id_servicio`) REFERENCES `dim_servicio` (`id_servicio`),
  ADD CONSTRAINT `fk_envio_tiempo` FOREIGN KEY (`id_tiempo`) REFERENCES `dim_tiempo` (`id_tiempo`),
  ADD CONSTRAINT `fk_envio_ubicacion` FOREIGN KEY (`id_ubicacion`) REFERENCES `dim_ubicacion` (`id_ubicacion`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
