-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-11-2026 a las 00:02:05
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
-- Base de datos: `nodo1_servientrega`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `envios`
--

CREATE TABLE `envios` (
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
-- Volcado de datos para la tabla `envios`
--

INSERT INTO `envios` (`id_envio`, `id_cliente`, `id_tiempo`, `id_ubicacion`, `id_servicio`, `id_estado`, `fecha_prometida`, `fecha_entrega`, `tiempo_entrega_horas`, `cantidad_paquetes`) VALUES
(1001, 1, 1, 1, 1, 1, '2025-11-03', '2025-11-02', 24.00, 1),
(1002, 2, 2, 2, 2, 1, '2025-11-05', '2025-11-05', 72.00, 2),
(1005, 2, 5, 1, 3, 4, '2025-11-09', '2025-11-10', 120.00, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `envios`
--
ALTER TABLE `envios`
  ADD PRIMARY KEY (`id_envio`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
