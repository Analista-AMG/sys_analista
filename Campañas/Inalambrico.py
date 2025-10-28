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

# Configurar logging
logging.basicConfig(
    filename='Campañas.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def Campaña_Inalambrico(fecha_inicio, fecha_fin):
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
    tables = ["TblFotosInalambricoExcel"]

    with engine.connect() as connection:
        with connection.begin() as transaction:
            for table in tables:
                connection.execute(text(f"DELETE FROM {table}"))
                logging.info(f"Contenido eliminado de la tabla {table}")

    ################################################################################################
    # Convertir strings de fechas
    fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dia_inicio = fecha_ini.day
    dia_fin = fecha_f.day
    año = fecha_f.year
    mes = fecha_f.month
    mesNombre = fecha_f.strftime("%B").capitalize()

    # Limpia el log existente antes de una nueva ejecución
    open('Campañas.log', 'w', encoding='utf-8').close()
    logging.info(f"Iniciando nueva ejecución para fechas: {fecha_inicio} a {fecha_fin}")
    ################################################################################################
    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_Inalambrico = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Fotos Inalambrico\{mesNombre}\FotosInalambrico{dia:02d}.csv"

        if os.path.exists(ruta_Inalambrico):
            try:
                dtype_especifico = {
                    'DNI_TECN': str
                }


                df_merged_Inalambrico = pd.read_csv(ruta_Inalambrico,sep=',',dtype=dtype_especifico) #separador de , en el CSV#

                df_merged_Inalambrico.columns = [normalize_column_name(col) for col in df_merged_Inalambrico.columns]

                df_merged_Inalambrico['hora_inicio_contrata'] = df_merged_Inalambrico['hora_inicio_contrata'].apply(parse_fecha) 
                df_merged_Inalambrico['hora_inicio_call_center'] = df_merged_Inalambrico['hora_inicio_call_center'].apply(parse_fecha) 
                df_merged_Inalambrico['hora_fin_call_center'] = df_merged_Inalambrico['hora_fin_call_center'].apply(parse_fecha)  

                with engine.connect() as connection:
                    df_merged_Inalambrico.to_sql('TblFotosInalambricoExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Alambrico cargado exitosamente para el día {dia}: {ruta_Inalambrico}")
            except Exception as e:
                logging.error(f"Error procesando archivo Alambrico {ruta_Inalambrico} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Alambrico no encontrado para el día {dia}: {ruta_Inalambrico}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_CampañaInalambrico_rango', parametros)
        conexion.commit()
        logging.info("Procedimiento almacenado Sp_CampañaInalambrico_rango ejecutado correctamente.")
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logging.error(f"Error en la ejecución del procedimiento almacenado: {error_details}")
        return f"Error en la obtención de datos: {error_details}"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
