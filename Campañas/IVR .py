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

def Campaña_TOA_prueba(fecha_inicio, fecha_fin):
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
    tables = ["TblClaroToaexcel", "TblIvrCalidadExcel", "TblDeliveryExcel"]

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
    ################################################################################################
    # Consulta a Navicat
    conexion = conectar_bdStores_Intranet()
    cursor_navicat = conexion.cursor()

    query = f"""
        SELECT DISTINCT 
            `N de pedido`, `Nombre del Cliente`, `DNI Cliente`, `Telefono del cliente`, `Nombre Motorizado`, `Empresa`, `Teléfono del motorizado`, 
            `Tipo de pago`, `ID de pago`, `Monto a cobrar`, `Tipo de tarjeta`, `Gestion`, `Resultado`, `Sub resultado`, `Observacion`,	
            DATE_FORMAT(`Hora inicio`, '%H:%i:%s') as `Hora inicio`,
            DATE_FORMAT(`Hora fin`, '%H:%i:%s') as `Hora fin`,
            `Asesor`, `TMO`,
            DATE_FORMAT(STR_TO_DATE(Fecha, '%d/%m/%Y'), '%Y-%m-%d') as Fecha
        FROM vista_reporte_ivr 
        WHERE DATE_FORMAT(STR_TO_DATE(Fecha, '%d/%m/%Y'), '%Y-%m-%d') BETWEEN '{fecha_ini.strftime('%Y-%m-%d')}' AND '{fecha_f.strftime('%Y-%m-%d')}'
    """

    cursor_navicat.execute(query)
    datos_navicat = cursor_navicat.fetchall()
    columnas = [desc[0] for desc in cursor_navicat.description]
    df_navicat = pd.DataFrame(datos_navicat, columns=columnas)
    df_navicat.columns = [normalize_column_name(col) for col in df_navicat.columns]

    motor = conectar_bdCargaExcel()
    df_navicat.to_sql('TblIvrCalidadExcel', motor, if_exists='append', index=False)
    logging.info("Datos de IVR cargados correctamente en TblIvrCalidadExcel")

    ###############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f, mes, año)
        cursor.callproc('Sp_CampañaDelivery_Rango', parametros)
        conexion.commit()
        logging.info("Procedimiento almacenado Sp_CampañaDelivery_Rango ejecutado correctamente.")
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
    