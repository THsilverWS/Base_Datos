USE DataSalud;
GO

TRUNCATE TABLE dbo.stg_vigilancia_minsa;
TRUNCATE TABLE dbo.Notificacion_Epidemiologica;
PRINT '>> Tablas staging y Notificacion_Epidemiologica vaciadas para carga limpia (evita duplicados).';
GO

PRINT '>> Cargando dataset de DENGUE (2000-2024)...';

BULK INSERT dbo.vw_stg_vigilancia_minsa
FROM 'C:\Users\Silver\Desktop\Grupo5_CIIN1021P_EF_REPO\01_datos\datos_abiertos_vigilancia_dengue_2000_2024.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001',
    TABLOCK
);
PRINT '>> Dengue cargado con éxito.';
GO

PRINT '>> Cargando dataset de LEISHMANIASIS (2000-2024)...';

BULK INSERT dbo.vw_stg_vigilancia_minsa
FROM 'C:\Users\Silver\Desktop\Grupo5_CIIN1021P_EF_REPO\01_datos\datos_abiertos_vigilancia_leishmaniosis_2000_2024.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001',
    MAXERRORS = 50,
    TABLOCK
);
PRINT '>> Leishmaniasis cargado con éxito.';
GO

DECLARE @total INT = (SELECT COUNT(*) FROM dbo.stg_vigilancia_minsa);

INSERT INTO dbo.Log_Auditoria (nombre_tabla, operacion, usuario, fecha_evento, cantidad_filas, detalle_evento)
VALUES (
    'stg_vigilancia_minsa',
    'CARGA_CSV',
    SYSTEM_USER,
    GETDATE(),
    @total,
    CONCAT('Carga masiva completada desde archivos CSV. Total en staging: ', @total)
);
GO

SELECT TOP 5 id_caso, departamento, enfermedad, ano, semana, diagnostic 
FROM dbo.stg_vigilancia_minsa;

SELECT enfermedad, COUNT(*) AS total_registros 
FROM dbo.stg_vigilancia_minsa 
GROUP BY enfermedad;

SELECT COUNT(*) AS total_general_staging FROM dbo.stg_vigilancia_minsa;
GO

PRINT '>> [04_carga_datos_csv.sql] Carga a Staging completada.';
PRINT '>> Migrando datos validados desde Staging hacia la tabla oficial Notificacion_Epidemiologica...';
GO

-- Ingesta controlada y validación de reglas clínicas hacia la tabla oficial
EXEC dbo.sp_IngestarDesdeStaging;
GO

PRINT '>> Verificando registros en Notificacion_Epidemiologica...';
SELECT COUNT(*) AS total_general_notificacion FROM dbo.Notificacion_Epidemiologica;

SELECT TOP 5 
    id_notificacion, 
    departamento, 
    provincia, 
    distrito, 
    enfermedad, 
    ano, 
    semana, 
    diagnostico_cie10, 
    edad, 
    sexo 
FROM dbo.Notificacion_Epidemiologica;
GO

PRINT '>> [04_carga_datos_csv.sql] Carga masiva e ingesta a Notificacion_Epidemiologica finalizada y verificada con éxito.';
GO
