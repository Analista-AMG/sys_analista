import sys
sys.path.append('v:\web')
import pandas as pd
from Campañas.funcion import *
from conexion import *
from unidecode import unidecode
from collections import Counter
from datetime import datetime, date
from deep_translator import GoogleTranslator
from datetime import datetime, date
import os
import locale
from sqlalchemy import text
import logging

# Configurar logging
logging.basicConfig(
    filename='Campañas.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

fecha_f='2025-07-21'
hoy = fecha_f
ayer= hoy  # Ya es un objeto date
#mesNombre = hoy.strftime("%B").capitalize()
#mes = hoy.month
#año = hoy.year
conexion = conectar_bdStores_Navicat3()
cursor_navicat = conexion.cursor() #Con el cursor puedes hacer consultas a la base de datos

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
query = f"""
SELECT `FECHA DE INICIO`, `FECHA FINAL`, `FECHA REGISTRO`, `CANAL`, `ESCALA DE SATISFACCION`, 
    `RAZON_PRINCIPAL`, `NO SOLUCIONARON MI RECLAMO O EL PROBLEMA PERSISTE`, 
    `EL SERVICIO TÉCNICO NO FUE ÓPTIMO`, `FUE DIFICIL CONTACTAR A CLARO , GENERACION DE VISITA`, 
    `NO CUMPLIMIENTO DE HORARIO Y/O FECHA`, `ATENCION DE LOS TECNICOS`, `COMENTARIO CLIENTE`, 
    `ESTADO INICIAL`, `SOT`, `DEPARTAMENTO_1`, `ESTADO CLIENTE`, `CLIENTE_S`, `CONTRATISTA_S`, 
    `TIPO DE TRABAJO`, `PROCESO`, `DEPARTAMENTO_2`, `PROVINCIA_S`, `DISTRITO_S`, `REGION`, 
    `DNI TECNICO`, `TECNICO`, `FECHA ATENDIDA`, `RAZON DE INSATISFACCION`, `RAZON ESPECIFICA`, 
    `ESTADO REVISION`, `AREA_DERIVADA_SOLUCION`, `INCONVENIENTE_REPORTADO_QUALTRICS`, 
    `FECHA ULTIMO ESTADO`, `OBSERVACION`, 
    CASE
    WHEN `TIPO DE SOLUCION` = NULL THEN NULL
    WHEN `TIPO DE SOLUCION` = '' THEN NULL
    ELSE `TIPO DE SOLUCION`
    END AS `TIPO DE SOLUCION`,
            `TIPO_ACCESO`,
            CASE
    WHEN `CONTACTABILIDAD` = NULL THEN NULL
    WHEN `CONTACTABILIDAD` = '' THEN NULL
    ELSE `CONTACTABILIDAD`
    END AS `CONTACTABILIDAD`,
    `SOT_CUADRIILLA_2N`, `AGENDA`, `ESTADO_VISITA`, `ESCALA_COORD_VISITA`, `RAZON_SIN_VISITA`, 
    `COMENTARIO_SIN_VISITA`, `GESTOR_NPS`, `CELULAR_CLIENTE`, `TNPS_ESTADO`, `TNPS_SCORE`
FROM Encuestas_Satisfaccion_Cliente
WHERE date(`FECHA REGISTRO`) BETWEEN DATE_SUB('{fecha_f}', INTERVAL 30 DAY) AND '{fecha_f}'
"""
cursor_navicat.execute(query)
datos_navicat = cursor_navicat.fetchall()

columnas = [desc[0] for desc in cursor_navicat.description] #Nombres de las columnas

df_navicat = pd.DataFrame(datos_navicat,columns=columnas)
#df_navicat['fecha_ultimo_estado'] = df_navicat['fecha_ultimo_estado'].replace('0000-00-00', None)
df_navicat.columns = [normalize_column_name(col) for col in df_navicat.columns]
df_navicat['fecha_ultimo_estado'] = df_navicat['fecha_ultimo_estado'].replace('0000-00-00', None)

motor = conectar_bdCargaExcel()

with motor.connect() as connection:
# Iniciar una transacción explícita
    with connection.begin() as transaction:
        connection.execute(text(f"""DELETE
                                    FROM TblMesasoporteBD
                                    WHERE CONVERT(DATE,fecha_registro) BETWEEN DATEADD(DAY, -30,CONVERT(DATE,'{fecha_f}',120) ) AND CONVERT(DATE,'{fecha_f}',120)"""))
        transaction.commit()

df_navicat.to_sql('TblMesasoporteBD', motor, if_exists='append', index=False)