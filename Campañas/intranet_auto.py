import sys
sys.path.append(rf'\\SERVIDOR06\python\web')

import pandas as pd
from Campañas.funcion import *
from conexion import *
from unidecode import unidecode
from collections import Counter
from datetime import datetime, date
from deep_translator import GoogleTranslator
import os
import locale
from sqlalchemy import text
import logging
from datetime import date

try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
    except locale.Error:
        logging.warning("No se pudo establecer el locale en español. Se usará el predeterminado.")
            
engine = conectar_bdCargaExcel()

################################################################################################
# Eliminar información de las tablas Excel
tables = ["TblIvrCalidadExcel","TblGestionBoFotosExcel","tblValidacionRemotaExcel"]

with engine.connect() as connection:
    with connection.begin() as transaction:
        for table in tables:
            connection.execute(text(f"DELETE FROM {table}"))
            logging.info(f"Contenido eliminado de la tabla {table}")

################################################################################################
# Convertir strings de fechas
fecha_actual = datetime.now()
fecha_f = fecha_actual.strftime("%Y-%m-%d")

################################################################################################
# Consulta a Navicat
conexion = conectar_bdStores_Intranet()
cursor_navicat = conexion.cursor()

query = f"""
    select DISTINCT 
            `N de pedido`, `Nombre del Cliente`, `DNI Cliente`, `Telefono del cliente`, `Nombre Motorizado`, `Empresa`, `Teléfono del motorizado`, 
            `Tipo de pago`, `ID de pago`, `Monto a cobrar`, `Tipo de tarjeta`, `Gestion`, `Resultado`, `Sub resultado`, `Observacion`,	
            DATE_FORMAT(`Hora inicio`, '%H:%i:%s') as `Hora inicio`,
            DATE_FORMAT(`Hora fin`, '%H:%i:%s') as `Hora fin`,
            `Asesor`, `TMO`,
            DATE_FORMAT(STR_TO_DATE(Fecha, '%d/%m/%Y'), '%Y-%m-%d') as Fecha
    FROM vista_reporte_ivr 
    WHERE DATE_FORMAT(STR_TO_DATE(Fecha, '%d/%m/%Y'), '%Y-%m-%d') = '{fecha_f}' 
"""
cursor_navicat.execute(query)
datos_navicat = cursor_navicat.fetchall()
columnas = [desc[0] for desc in cursor_navicat.description]
df_navicat = pd.DataFrame(datos_navicat, columns=columnas)
df_navicat.columns = [normalize_column_name(col) for col in df_navicat.columns]

motor = conectar_bdCargaExcel()
df_navicat.to_sql('TblIvrCalidadExcel', motor, if_exists='append', index=False)
logging.info("Datos de IVR cargados correctamente en TblIvrCalidadExcel")

################################################################################################
# Consulta a Navicat
conexion = conectar_bdStores_Intranet()
cursor_navicat = conexion.cursor()

query = f"""
            select 
            `SOT`,	`SALESYS`,	`OPERADOR`,	
            DATE_FORMAT(STR_TO_DATE(`FECHA BASE`	 ,'%d/%m/%Y'), '%Y-%m-%d') as `FECHA BASE`,
            DATE_FORMAT(STR_TO_DATE(`FECHA INICIO`,	 '%d/%m/%Y'), '%Y-%m-%d') as `FECHA INICIO`,
            DATE_FORMAT(STR_TO_DATE(`FECHA FIN`		 ,'%d/%m/%Y'), '%Y-%m-%d') as `FECHA FIN`,
            `FAT`,	`ROSETA`,	`DIFERENCIA`,	`PLANO`,	`NUMERO FAT`,	`BORNE LIBRE`,	`ROSETA OPTICA`,	`COBERTURA`
            from vista_validacion_dp 
            where 
            DATE_FORMAT(STR_TO_DATE(`FECHA BASE`, '%d/%m/%Y'), '%Y-%m-%d') = '{fecha_f}';
"""
cursor_navicat.execute(query)
datos_navicat = cursor_navicat.fetchall()
columnas = [desc[0] for desc in cursor_navicat.description]
df_navicat = pd.DataFrame(datos_navicat, columns=columnas)
df_navicat.columns = [normalize_column_name(col) for col in df_navicat.columns]

motor = conectar_bdCargaExcel()
df_navicat.to_sql('TblGestionBoFotosExcel', motor, if_exists='append', index=False)
logging.info("Datos de IVR cargados correctamente en TblIvrCalidadExcel")

################################################################################################
# Consulta a Navicat
conexion = conectar_bdStores_Intranet()
cursor_navicat = conexion.cursor()

query = f"""
select 
`NOMBRE CONTRATA`,	`CLIENTE`,	`SOT`,	`ESTADO AGENDAMIENTO`,	`TIPO DE TRABAJO`,	`DEPARTAMENTO`,	`CUSTOMER_ID`,	`SALESYS`,	`OPERADOR`,	`RESPONSABLE`,	`VALIDACION`,	`SUBESTADO`,	
`MOTIVO`,	`SKYWAY`,	`AFECTACION`,	`DESALINEACION`,	`SERVICIO AFECTADO`,	`INCONVENIENTE`,	`OBSERVACION`,	
DATE_FORMAT(STR_TO_DATE(`FECHA INICIO`, '%d/%m/%Y %H:%i:%s'), '%Y-%m-%d %H:%i:%s') AS `FECHA INICIO`,
DATE_FORMAT(STR_TO_DATE(`FECHA FIN`, '%d/%m/%Y %H:%i:%s'), '%Y-%m-%d %H:%i:%s') AS `FECHA FIN`,
TIME_FORMAT(`TMO`, '%H:%i:%s') AS `TMO`
from vista_validacion_remota 
where DATE_FORMAT(STR_TO_DATE(`FECHA INICIO`, '%d/%m/%Y'), '%Y-%m-%d') = '{fecha_f}';
"""
cursor_navicat.execute(query)
datos_navicat = cursor_navicat.fetchall()
columnas = [desc[0] for desc in cursor_navicat.description]
df_navicat = pd.DataFrame(datos_navicat, columns=columnas)
df_navicat.columns = [normalize_column_name(col) for col in df_navicat.columns]

motor = conectar_bdCargaExcel()
df_navicat.to_sql('tblValidacionRemotaExcel', motor, if_exists='append', index=False)
logging.info("Datos de IVR cargados correctamente en TblIvrCalidadExcel")


###############################################################################################
conexion = conectar_bdStores()

try:
    cursor = conexion.cursor()
    
    # Llamada al procedimiento almacenado sin parámetros
    cursor.callproc('sp_intranet_GetDate')
    conexion.commit()  # ⚠️ Solo si el SP realiza operaciones de escritura (INSERT, UPDATE, DELETE)

    logging.info("Procedimiento almacenado Sp_CampañaDelivery_Rango ejecutado correctamente.")

except Exception as e:
    import traceback
    error_details = traceback.format_exc()
    logging.error(f"Error en la ejecución del procedimiento almacenado: {error_details}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conexion' in locals() and conexion:
        conexion.close()