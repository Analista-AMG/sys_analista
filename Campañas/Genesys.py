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
import warnings

# Configura logging como ya tienes
logging.basicConfig(
    filename='Campañas.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Redirige los warnings de Python al logging
def custom_warning_to_log(message, category, filename, lineno, file=None, line=None):
    logging.warning(f'{category.__name__}: {message} ({filename}:{lineno})')

warnings.showwarning = custom_warning_to_log


def Campaña_Genesys_General(fecha_inicio, fecha_fin):
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
    tables = ["TblEstadoAgenteGenesysExcel", "TblEstadoAgenteGenesysDetalleExcel"]

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
    #open('Campañas.log', 'w', encoding='utf-8').close()
    logging.info(f"Iniciando nueva ejecución para fechas: {fecha_inicio} a {fecha_fin}")
    ################################################################################################
    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_EstadoAgente = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Genesys\{mesNombre}\Estatus\Estatus{dia:02d}.csv"

        if os.path.exists(ruta_EstadoAgente):
            try:
                df_merged_EstadoAgente = pd.read_csv(ruta_EstadoAgente, sep=',', encoding='utf-8')
                df_merged_EstadoAgente.columns = [normalize_column_name(col) for col in df_merged_EstadoAgente.columns]

                df_merged_EstadoAgente['inicio_del_intervalo'] = df_merged_EstadoAgente['inicio_del_intervalo'].apply(parse_fecha_genesys)
                df_merged_EstadoAgente['fin_del_intervalo'] = df_merged_EstadoAgente['fin_del_intervalo'].apply(parse_fecha_genesys)
                df_merged_EstadoAgente['iniciar_sesion'] = df_merged_EstadoAgente['iniciar_sesion'].apply(parse_fecha_genesys)
                df_merged_EstadoAgente['cerrar_sesion'] = df_merged_EstadoAgente['cerrar_sesion'].apply(parse_fecha_genesys)

                with engine.connect() as connection:
                    df_merged_EstadoAgente.to_sql('TblEstadoAgenteGenesysExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Genesys cargado exitosamente para el día {dia}: {ruta_EstadoAgente}")
            except Exception as e:
                logging.error(f"Error procesando archivo Genesys {ruta_EstadoAgente} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Genesys no encontrado para el día {dia}: {ruta_EstadoAgente}")

    ################################################################################################
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_EstadoAgenteDetalle = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Genesys\{mesNombre}\Estatus_Detalle\agenteDetalle{dia:02d}.csv"


        if os.path.exists(ruta_EstadoAgenteDetalle):
            try:

                df_merged_EstadoAgenteDetalle = pd.read_csv(ruta_EstadoAgenteDetalle, sep=',', encoding='utf-8')
                df_merged_EstadoAgenteDetalle.columns = [normalize_column_name(col) for col in df_merged_EstadoAgenteDetalle.columns]

                df_merged_EstadoAgenteDetalle['inicio_del_intervalo'] = df_merged_EstadoAgenteDetalle['inicio_del_intervalo'].apply(parse_fecha_genesys)
                df_merged_EstadoAgenteDetalle['fin_del_intervalo'] = df_merged_EstadoAgenteDetalle['fin_del_intervalo'].apply(parse_fecha_genesys)
                df_merged_EstadoAgenteDetalle['hora_de_inicio'] = df_merged_EstadoAgenteDetalle['hora_de_inicio'].apply(parse_fecha_laraigo)
                df_merged_EstadoAgenteDetalle['hora_de_finalizacion'] = df_merged_EstadoAgenteDetalle['hora_de_finalizacion'].apply(parse_fecha_laraigo)

                df_merged_EstadoAgenteDetalle['duracion'] = pd.to_timedelta(df_merged_EstadoAgenteDetalle['duracion']) 
                df_merged_EstadoAgenteDetalle['duracion'] = df_merged_EstadoAgenteDetalle['duracion'].dt.total_seconds() 

                with engine.connect() as connection:
                    df_merged_EstadoAgenteDetalle.to_sql('TblEstadoAgenteGenesysDetalleExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Genesys General cargado exitosamente para el día {dia}: {df_merged_EstadoAgenteDetalle}")
            except Exception as e:
                logging.error(f"Error procesando archivo Genesys General {df_merged_EstadoAgenteDetalle} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Genesys General no encontrado para el día {dia}: {df_merged_EstadoAgenteDetalle}")

   
    ###############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_EstadoAgenteGenesys_rango', parametros)
        conexion.commit()
        logging.info("Procedimiento almacenado Sp_EstadoAgenteGenesys_rango ejecutado correctamente.")
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
