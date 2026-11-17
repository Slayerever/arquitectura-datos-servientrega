USE dw_servientrega;

CREATE OR REPLACE VIEW vw_envios_anonimizados AS
SELECT
    h.id_envio,
    CONCAT('CLI-', LPAD(h.id_cliente, 4, '0')) AS codigo_cliente_anonimo,
    c.tipo_cliente,
    t.fecha AS fecha_envio,
    u.ciudad_origen,
    u.ciudad_destino,
    s.tipo_servicio,
    e.estado_envio,
    h.fecha_prometida,
    h.fecha_entrega,
    h.tiempo_entrega_horas,
    h.cantidad_paquetes
FROM hechos_envios h
INNER JOIN dim_cliente c ON h.id_cliente = c.id_cliente
INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
INNER JOIN dim_ubicacion u ON h.id_ubicacion = u.id_ubicacion
INNER JOIN dim_servicio s ON h.id_servicio = s.id_servicio
INNER JOIN dim_estado e ON h.id_estado = e.id_estado;

CREATE ROLE IF NOT EXISTS 'rol_etl_carga';
CREATE ROLE IF NOT EXISTS 'rol_analista_bi';
CREATE ROLE IF NOT EXISTS 'rol_auditor_calidad';

GRANT SELECT, INSERT, UPDATE ON staging_servientrega.* TO 'rol_etl_carga';
GRANT SELECT ON dw_servientrega.vw_envios_anonimizados TO 'rol_analista_bi';
GRANT SELECT ON dw_servientrega.* TO 'rol_auditor_calidad';

DROP USER IF EXISTS 'analista_servi'@'localhost';
CREATE USER 'analista_servi'@'localhost' IDENTIFIED BY 'Analista2026*';
GRANT 'rol_analista_bi' TO 'analista_servi'@'localhost';
SET DEFAULT ROLE 'rol_analista_bi' FOR 'analista_servi'@'localhost';

DROP USER IF EXISTS 'usuario_sin_permisos'@'localhost';
CREATE USER 'usuario_sin_permisos'@'localhost' IDENTIFIED BY 'Bloqueado2026*';

FLUSH PRIVILEGES;