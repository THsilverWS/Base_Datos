# DataSalud Perú — DIRESA La Libertad
## Sistema Integrado de Base de Datos Segura, Automatizada y Analítica (MINSA)

**Curso:** Bases de Datos Avanzadas y Big Data (CIIN1021P) | Ciclo 2026-2  
**Institución:** Universidad Privada del Norte (UPN)  
**Grupo:** Grupo 5  
**Docente:** Jorge Ricardo Pérez Vigil  

### Integrantes del Equipo
* CRUZADO ARROYO, JOAQUIN MATHIAS (N00467227)
* GOMEZ LLERENA, FABRIZIO MATHÍAS (N00498473)
* JUAREZ GARRIDO, JHON ALBERTO (N00475124)
* MIRANDA AMAYA, ALINA JAQUELINE (N00476960)
* PAREDES PACHERRE, CARLOS ADRIAN (N00483352)
* RODRIGUEZ PIZAN, MATHIAS FELIPE (N00467212)

---

## 📌 ¿De qué trata el proyecto?
El proyecto implementa una solución de datos de extremo a extremo para la **DIRESA La Libertad** que automatiza la ingesta de datos, garantiza la seguridad bajo la **Ley N.° 29733** (Protección de Datos Personales), integra persistencia híbrida **SQL y NoSQL (MongoDB)**, construye un **Data Warehouse dimensional (Ralph Kimball)** con procesos ETL y permite el análisis visual interactivo en **Power BI** y procesamiento masivo con **Apache PySpark**.

---

## 📁 Estructura del Repositorio

```text
Grupo5_CIIN1021P_EF_REPO/
│
├── 01_datos/             --> Muestras de prueba y diagnóstico cuantificado de calidad de datos
├── 02_automatizacion/    --> DDL, SPs, triggers de auditoría/integridad y pruebas en SQL Server
├── 03_seguridad/         --> Roles RBAC (Ley 29733), políticas de respaldo, restore y optimización
├── 04_nosql/             --> Datos clínicos semiestructurados JSON y operaciones CRUD en MongoDB
├── 05_dw_etl/            --> Modelo dimensional (Kimball), paquete SSIS de Visual Studio y ETL en Python
├── 06_dashboard/         --> Dashboard oficial en Power BI Desktop (.pbix), consultas OLAP y medidas DAX
├── 07_bigdata/           --> Cuaderno PySpark para Google Colab y script de benchmark de escalabilidad
│
├── 00_borrar_bases_de_datos.sql  --> Script para reiniciar el entorno de pruebas en SQL Server
├── README.md                     --> Documentación técnica y guía de ejecución del proyecto
├── requirements.txt              --> Dependencias de Python (pymongo, pandas)
└── setup.py                      --> Script para instalación rápida de dependencias
```

---

## 🚀 Guía Rápida de Ejecución Paso a Paso

### Paso 0: Reinicio del Entorno (Opcional)
Si deseas limpiar cualquier base de datos o login previo para iniciar pruebas desde cero, ejecuta en SQL Server Management Studio (SSMS):
```sql
00_borrar_bases_de_datos.sql
```

### Paso 1: Instalación de Dependencias
Instala las librerías necesarias con un solo comando en la terminal:
```bash
python setup.py
```

### Paso 2: Diagnóstico de Calidad de Datos
Analiza los registros epidemiológicos, detecta campos nulos y cuenta duplicados:
```bash
python 01_datos/diagnostico_calidad.py
```
*Los resultados se guardan automáticamente en `01_datos/diagnostico_calidad_resultado.txt`.*

### Paso 3: Automatización y Control Transaccional (SQL Server)
En **SSMS**, conectado a tu instancia local (`.` o `localhost`), ejecuta en orden:
1. `02_automatizacion/01_ddl_tablas_y_log.sql`: Crea la base de datos `DataSalud`, tablas de staging, tabla oficial y tabla inmutable `Log_Auditoria`.
2. `02_automatizacion/02_stored_procedures.sql`: Compila la función de etapas de vida (`fn_ClasificarCursoVida`), triggers de auditoría e integridad y los procedimientos almacenados transaccionales (`sp_IngestarDesdeStaging`, `sp_ValidarYRegistrarCaso`).
3. `02_automatizacion/03_pruebas_automatizacion.sql`: Ejecuta las 7 pruebas automáticas (bloqueo de semanas inválidas, reversión con savepoint y registro de auditoría).
4. `02_automatizacion/04_carga_datos_csv.sql`: Carga masiva con `BULK INSERT` a staging.

### Paso 4: Seguridad, Respaldo y Rendimiento
En SSMS, ejecuta en orden:
1. `03_seguridad/01_roles_y_permisos.sql`: Crea los 3 roles (`rol_administrador`, `rol_analista`, `rol_auditor`), logins con contraseñas seguras y valida permisos con `EXECUTE AS`.
2. `03_seguridad/02_politica_respaldo.sql`: Genera los respaldos Full y Diferencial en disco.
3. `03_seguridad/03_restauracion_prueba.sql`: Restaura la copia de seguridad en `DataSalud_RestoreTest` en modo `NORECOVERY` y `RECOVERY`.
4. `03_seguridad/04_optimizacion_indices.sql`: Crea el índice no agrupado `IX_Notificacion_Enfermedad_Ano_Semana` y mide la aceleración de consultas (Index Seek).

### Paso 5: Persistencia NoSQL (MongoDB)
Con el servicio de MongoDB iniciado localmente, ejecuta el script interactivo CRUD:
```bash
python 04_nosql/operaciones_crud_mongodb.py
```
*Ejecuta las operaciones de inserción masiva (Create), lectura de pacientes graves (Read), actualización de plaquetas (Update) y eliminación controlada (Delete).*

### Paso 6: Data Warehouse y Pipeline ETL
Para construir el modelo dimensional en estrella y poblar las 5 dimensiones y la tabla de hechos, dispones de dos alternativas equivalentes:
* **Opción A (Rápida por Terminal):**
  ```bash
  python 05_dw_etl/etl_python_simple.py
  ```
* **Opción B (Visual Studio SSIS):**
  Abre la solución `05_dw_etl/ETL/ETL.slnx`, haz doble clic en `Package.dtsx` y presiona **Iniciar (Start)**.

### Paso 7: Dashboard y Análisis OLAP (Power BI)
* **Visualización en Power BI Desktop:**
  Abre el archivo `06_dashboard/DataSalud_Dashboard.pbix` en Power BI Desktop. El archivo está configurado en **Modo Importación**, por lo que contiene el modelo semántico cargado, las relaciones activas y las medidas DAX oficiales (`Total Casos`, `Tasa Severidad Porcentual`, `Presión Asistencial por Centro`).
* **Consultas Multidimensionales OLAP en SQL Server:**
  Ejecuta `06_dashboard/consultas_olap_sql.sql` en SSMS para ver las operaciones de agregación con `ROLLUP` y `CUBE`.

### Paso 8: Procesamiento Big Data (Apache PySpark)
* **Ejecución Rápida en Terminal:**
  ```bash
  python 07_bigdata/analisis_bigdata_script.py
  ```
* **Ejecución en Google Colab:**
  1. Entra a [colab.research.google.com](https://colab.research.google.com).
  2. Sube el cuaderno `07_bigdata/analisis_bigdata_pyspark.ipynb`.
  3. Menú **Entorno de ejecución ➔ Ejecutar todo**. El cuaderno instala PySpark automáticamente y ejecuta los 3 objetos de Spark (DataFrames, SparkSQL y RDDs map/reduce).