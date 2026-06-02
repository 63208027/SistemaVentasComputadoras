-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-06-2026 a las 10:26:26
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detallepedidos`
--

CREATE TABLE `detallepedidos` (
  `id_detalle` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detallepedidos`
--

INSERT INTO `detallepedidos` (`id_detalle`, `id_pedido`, `id_producto`, `cantidad`, `precio_unitario`, `total`) VALUES
(11, 6, 4, 1, 2.00, 2.00),
(12, 6, 5, 1, 200.00, 200.00),
(13, 7, 4, 1, 2.00, 2.00),
(14, 7, 5, 1, 200.00, 200.00),
(15, 8, 9, 1, 23.00, 23.00),
(16, 9, 5, 1, 200.00, 200.00),
(17, 10, 6, 1, 3.00, 3.00),
(18, 11, 7, 12, 12.00, 144.00),
(19, 12, 4, 12, 2.00, 24.00),
(20, 12, 5, 12, 200.00, 2400.00),
(21, 12, 6, 12, 3.00, 36.00),
(22, 13, 4, 12, 2.00, 24.00),
(23, 13, 5, 12, 200.00, 2400.00),
(24, 13, 6, 12, 3.00, 36.00),
(25, 14, 4, 12, 2.00, 24.00),
(26, 14, 5, 12, 200.00, 2400.00),
(27, 15, 8, 12, 300.00, 3600.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_pedido` datetime DEFAULT current_timestamp(),
  `estado` enum('pendiente','completado','cancelado') DEFAULT 'pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `id_usuario`, `fecha_pedido`, `estado`) VALUES
(6, 5, '2024-12-04 03:22:40', 'completado'),
(7, 5, '2024-12-04 03:23:25', 'pendiente'),
(8, 5, '2024-12-04 03:25:37', 'pendiente'),
(9, 5, '2024-12-04 03:25:45', 'pendiente'),
(10, 5, '2024-12-04 03:25:52', 'pendiente'),
(11, 5, '2024-12-04 03:39:29', 'completado'),
(12, 5, '2024-12-04 03:39:44', 'completado'),
(13, 5, '2024-12-04 03:39:57', 'pendiente'),
(14, 5, '2025-06-12 22:16:41', 'completado'),
(15, 10, '2026-06-01 03:40:11', 'completado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp(),
  `estado` enum('disponible','agotado') DEFAULT 'disponible',
  `categoria` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `precio`, `cantidad`, `imagen`, `fecha_registro`, `estado`, `categoria`) VALUES
(4, 'Laptop Lenovo ', 'Laptop Ryzen 5, 8GB RAM, SSD 512GB', 4500.00, 10, 'laptop_lenovo.jpg', '2024-12-04 01:12:46', 'disponible', 'laptops'),
(5, 'Laptop HP', 'Intel Core i5, 8GB RAM', 5200.00, 10, 'LaptopHP.jpeg', '2024-12-04 01:17:45', 'disponible', 'laptops'),
(6, 'PC Gamer Ryzen 5', 'RTX 4060, 16GB RAM', 8500.00, 10, 'PC gamer.webp', '2024-12-04 01:18:07', 'disponible', 'computadoras'),
(7, 'Monitor Samsung 24\"', 'Full HD 24 pulgadas', 1200.00, 20, 'Monitor.jpg', '2024-12-04 02:21:33', 'disponible', 'computadoras'),
(8, 'Teclado Mecánico RGB', 'Teclado gamer retroiluminado', 300.00, 3, 'teclado.jpg', '2024-12-04 02:21:58', 'disponible', 'accesorios'),
(9, 'Mouse Logitech G203', 'Mouse óptico gamer', 100.00, 20, 'mouse.jpg', '2024-12-04 02:22:22', 'disponible', 'accesorios'),
(10, 'Impresora Epson L3250', 'Impresora multifuncional WiFi', 2000.00, 5, 'impresora.jpg', '2024-12-04 03:42:47', 'disponible', 'accesorios'),
(11, 'Disco SSD 1TB', 'Unidad SSD SATA 1TB', 550.00, 20, 'discoSSD.webp', '2024-12-04 03:43:12', 'disponible', 'accesorios');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('cliente','administrador') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `email`, `contraseña`, `rol`) VALUES
(4, 'admin', 'admin@gmail.com', 'pbkdf2:sha256:1000000$pbEO43zCT4oFgr39$5bc4d3f9201e19e370b75080470f121df0e87a2fd3fc0c88c870bd273684064c', 'administrador'),
(5, 'Cliente ', 'cliente@gmail.com', 'pbkdf2:sha256:1000000$IOV9TXhO5tw3MazY$d60ce917a1cd7cc4f4acb0960249412f56a58d289eccd2a5fe8dc87cad1d9b3f', 'cliente'),
(6, 'miguel', 'miguel@gmail.com', 'pbkdf2:sha256:1000000$ToJMYJYLTg4mrTYE$83d0450655a28252047591632a021fb23632504601551745542f9d822f41dec3', 'cliente'),
(7, 'jhonatan', 'jhonatan@gmail.com', 'pbkdf2:sha256:1000000$a4FsSzwNuBYuR63W$5092aef10ce39a1414f9cab0ff13ed4e9a3f2c053d6d6f18b68995723012d3b5', 'cliente'),
(8, 'jhon', 'jhon@gmail.com', 'pbkdf2:sha256:1000000$kVsw01YqnTTFlArI$1de32589d04577e3da49e5136dd22fda7d10bfc61a92e07fb53c9b07ddd2511c', 'cliente'),
(9, 'mariela', 'mariela@gmail.com', 'pbkdf2:sha256:1000000$9jqPTc07wXEBefJF$c0a9201f5e9b136df3b4825002ad36f948c50d459a40fe6798d455f10e64ba29', 'cliente'),
(10, 'Angel Limachi Ticona', 'angellimachiticona@gmail.com', 'pbkdf2:sha256:1000000$uKdDBbe96qpKBSIr$0af5970a3849f17ef1a05ca9b0f29cf5d3fbdefcefde93bc7882585fa72efebe', 'cliente');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `detallepedidos`
--
ALTER TABLE `detallepedidos`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `detallepedidos`
--
ALTER TABLE `detallepedidos`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detallepedidos`
--
ALTER TABLE `detallepedidos`
  ADD CONSTRAINT `detallepedidos_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  ADD CONSTRAINT `detallepedidos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
