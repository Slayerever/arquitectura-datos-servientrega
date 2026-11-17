# Arquitectura de Datos — Servientrega S.A.

Implementación integral de una arquitectura de datos empresarial para la gestión y análisis de operaciones logísticas de **Servientrega S.A.**, desarrollada para el curso de **Arquitectura de Datos (Ingeniería de Sistemas — UNIMINUTO Sede Soacha)**.

## Estructura del Repositorio

- `warehouse/`: Script DDL y DML del modelo dimensional en estrella (`dw_servientrega.sql`).
- `base de datos/`: Extracción multi-fuente (MariaDB, CSV, API DIVIPOLA DANE), carga en área temporal (`staging_servientrega.sql`), consulta federada entre puertos `3306` y `3307`, fragmentación horizontal/vertical y reconstrucción mediante `UNION ALL`.
- `gobernanza/`: Roles bajo principio de mínimo privilegio, vista anonimizada en cumplimiento de la Ley 1581 de 2012 (`gobernanza_roles.sql`) y validación automática de 6 reglas de calidad (`gobernanza_calidad.py`).
- `kdd_kpi_xa/`: Consultas pivote en SQL y Python (`kpi_pivote.py`), matriz de KPI (`matriz_kpi.csv`), transacción distribuida Two-Phase Commit con `XA START / PREPARE / COMMIT / ROLLBACK` (`transaccion_xa.py`) y cuaderno del proceso KDD (`kdd_servientrega.ipynb`).
- `dashboard/`: Aplicación web interactiva de visualización analítica desarrollada con Streamlit (`app_servientrega.py`).

## Requisitos e Instalación

1. Python 3.10 o superior.
2. Servidores de base de datos activos en puerto `3306` (MariaDB / XAMPP) y puerto `3307` (segundo nodo MySQL/MariaDB).
3. Instalar dependencias:
   ```bash
   pip install pandas sqlalchemy pymysql mysql-connector-python requests scikit-learn jupyter matplotlib streamlit

   Orden de Ejecución
Importar warehouse/dw_servientrega.sql, base de datos/staging_servientrega.sql y base de datos/nodo1_servientrega.sql en el servidor 3306.

Ejecutar gobernanza/gobernanza_roles.sql sobre dw_servientrega y validar con python gobernanza/gobernanza_calidad.py.

Poblar el segundo servidor (3307) ejecutando preparar_mysql8.py y distribuir_nodos.py.

Ejecutar python kdd_kpi_xa/kpi_pivote.py y python kdd_kpi_xa/transaccion_xa.py.

Iniciar el dashboard analítico:

Bash
python -m streamlit run dashboard/app_servientrega.py