USE dw_servientrega;

-- Consulta Pivote 1: Envíos por Ciudad Destino y Estado
SELECT
    u.ciudad_destino,
    COUNT(h.id_envio) AS total_envios,
    SUM(CASE WHEN e.estado_envio = 'Entregado' THEN 1 ELSE 0 END) AS entregados,
    SUM(CASE WHEN e.estado_envio = 'En transito' THEN 1 ELSE 0 END) AS en_transito,
    SUM(CASE WHEN e.estado_envio = 'Pendiente' THEN 1 ELSE 0 END) AS pendientes,
    SUM(CASE WHEN e.estado_envio = 'Devuelto' THEN 1 ELSE 0 END) AS devueltos
FROM hechos_envios h
INNER JOIN dim_ubicacion u ON h.id_ubicacion = u.id_ubicacion
INNER JOIN dim_estado e ON h.id_estado = e.id_estado
GROUP BY u.ciudad_destino
ORDER BY total_envios DESC;

-- Consulta Pivote 2: Paquetes por Cliente y Tipo de Servicio
SELECT
    c.nombre AS cliente,
    SUM(CASE WHEN s.tipo_servicio = 'Express' THEN h.cantidad_paquetes ELSE 0 END) AS paquetes_express,
    SUM(CASE WHEN s.tipo_servicio = 'Estandar' THEN h.cantidad_paquetes ELSE 0 END) AS paquetes_estandar,
    SUM(CASE WHEN s.tipo_servicio = 'Especial' THEN h.cantidad_paquetes ELSE 0 END) AS paquetes_especial,
    SUM(h.cantidad_paquetes) AS total_paquetes
FROM hechos_envios h
INNER JOIN dim_cliente c ON h.id_cliente = c.id_cliente
INNER JOIN dim_servicio s ON h.id_servicio = s.id_servicio
GROUP BY c.nombre
ORDER BY total_paquetes DESC;