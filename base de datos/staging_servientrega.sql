-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-11-2026 a las 00:02:21
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
-- Base de datos: `staging_servientrega`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stg_envios_csv`
--

CREATE TABLE `stg_envios_csv` (
  `id_envio` bigint(20) DEFAULT NULL,
  `fecha_envio` text DEFAULT NULL,
  `ciudad_origen` text DEFAULT NULL,
  `ciudad_destino` text DEFAULT NULL,
  `tipo_servicio` text DEFAULT NULL,
  `estado` text DEFAULT NULL,
  `peso_kg` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `stg_envios_csv`
--

INSERT INTO `stg_envios_csv` (`id_envio`, `fecha_envio`, `ciudad_origen`, `ciudad_destino`, `tipo_servicio`, `estado`, `peso_kg`) VALUES
(2001, '2025-11-06', 'Bogota', 'Medellin', 'Express', 'Entregado', 2.5),
(2002, '2025-11-07', 'Cali', 'Bogota', 'Estandar', 'En Transito', 3),
(2003, '2025-11-08', 'Bogota', 'Barranquilla', 'Especial', 'Entregado', 1.8),
(2004, '2025-11-09', 'Medellin', 'Cali', 'Express', 'Pendiente', 4.2),
(2005, '2025-11-10', 'Barranquilla', 'Bogota', 'Estandar', 'Entregado', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stg_envios_mariadb`
--

CREATE TABLE `stg_envios_mariadb` (
  `id_envio` bigint(20) DEFAULT NULL,
  `cliente` text DEFAULT NULL,
  `fecha_envio` text DEFAULT NULL,
  `ciudad_origen` text DEFAULT NULL,
  `ciudad_destino` text DEFAULT NULL,
  `tipo_servicio` text DEFAULT NULL,
  `estado_envio` text DEFAULT NULL,
  `tiempo_entrega_horas` double DEFAULT NULL,
  `cantidad_paquetes` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `stg_envios_mariadb`
--

INSERT INTO `stg_envios_mariadb` (`id_envio`, `cliente`, `fecha_envio`, `ciudad_origen`, `ciudad_destino`, `tipo_servicio`, `estado_envio`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1001, 'Comercial Andina S.A.S.', '2025-11-01', 'Bogota', 'Medellin', 'Express', 'Entregado', 24, 1),
(1004, 'Comercial Andina S.A.S.', '2025-11-04', 'Barranquilla', 'Cartagena', 'Estandar', 'En Transito', NULL, 3),
(1002, 'Distribuciones Central S.A.S.', '2025-11-02', 'Medellin', 'Bogota', 'Estandar', 'Entregado', 72, 2),
(1005, 'Distribuciones Central S.A.S.', '2025-11-05', 'Bogota', 'Medellin', 'Especial', 'Devuelto', 120, 1),
(1003, 'Carlos Ramirez', '2025-11-03', 'Cali', 'Bogota', 'Express', 'Entregado', 30, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stg_municipios_dane`
--

CREATE TABLE `stg_municipios_dane` (
  `cod_dpto` bigint(20) DEFAULT NULL,
  `dpto` text DEFAULT NULL,
  `cod_mpio` bigint(20) DEFAULT NULL,
  `nom_mpio` text DEFAULT NULL,
  `tipo_municipio` text DEFAULT NULL,
  `longitud` text DEFAULT NULL,
  `latitud` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `stg_municipios_dane`
--

INSERT INTO `stg_municipios_dane` (`cod_dpto`, `dpto`, `cod_mpio`, `nom_mpio`, `tipo_municipio`, `longitud`, `latitud`) VALUES
(5, 'ANTIOQUIA', 5001, 'MEDELLÍN', 'Municipio', '-75,581775', '6,246631'),
(5, 'ANTIOQUIA', 5002, 'ABEJORRAL', 'Municipio', '-75,428739', '5,789315'),
(5, 'ANTIOQUIA', 5004, 'ABRIAQUÍ', 'Municipio', '-76,064304', '6,632282'),
(5, 'ANTIOQUIA', 5021, 'ALEJANDRÍA', 'Municipio', '-75,141346', '6,376061'),
(5, 'ANTIOQUIA', 5030, 'AMAGÁ', 'Municipio', '-75,702188', '6,038708'),
(5, 'ANTIOQUIA', 5031, 'AMALFI', 'Municipio', '-75,077501', '6,909655'),
(5, 'ANTIOQUIA', 5034, 'ANDES', 'Municipio', '-75,878828', '5,657194'),
(5, 'ANTIOQUIA', 5036, 'ANGELÓPOLIS', 'Municipio', '-75,711389', '6,109719'),
(5, 'ANTIOQUIA', 5038, 'ANGOSTURA', 'Municipio', '-75,335116', '6,885175'),
(5, 'ANTIOQUIA', 5040, 'ANORÍ', 'Municipio', '-75,148355', '7,074703');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
