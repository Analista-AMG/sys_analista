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

def CargaNominaCorporativo(fecha_fin):
    
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

    if isinstance(fecha_fin, str):
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    elif isinstance(fecha_fin, datetime):
        fecha_f = fecha_fin.date()
    elif isinstance(fecha_fin, date):
        fecha_f = fecha_fin
    else:
        raise ValueError("fecha_fin debe ser str, datetime o date")

    hoy = fecha_f
    ayer= hoy  # Ya es un objeto date
    mesNombre = hoy.strftime("%B").capitalize()
    mes = hoy.month
    año = hoy.year

    engine = conectar_bdCargaExcel()
    with engine.connect() as connection:
        with connection.begin() as transaction:
            connection.execute(
                text("DELETE FROM tblNominaExcelv2")
            )
            transaction.commit()
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\Fotos_Corporativo\{año}\{mesNombre}\nomina_{hoy.strftime('%Y%m')}.xlsx"
    Ruta_Carpeta = archivo_excel.split("\\")[4]

    dataframes = []
    ultimo_log_hoja = None  # Para guardar el último mensaje de hoja agregada
    try:
        excel = pd.ExcelFile(archivo_excel)

        for hoja in excel.sheet_names:
            try:
                fecha_hoja = datetime.strptime(hoja, "%Y-%m-%d").date()

                if fecha_hoja.month == ayer.month and 1 <= fecha_hoja.day <= ayer.day:
                    
                    df = excel.parse(hoja, dtype={'DNI': str})
                    df.columns = [normalize_column_name(col) for col in df.columns]
                    if 'fecha' in df.columns:
                        df = df.drop(columns=['fecha'])
                    df['fecha'] = fecha_hoja
                    df = df.rename(columns={'campana': 'campaña', 'fecha_ingreso_campana': 'fecha_ingreso_campaña'})
                    df['region'] = None
                    df = df.loc[:, ~df.columns.duplicated()]
                    df["hora_entrada"] = df["hora_entrada"].apply(lambda x: str(x).split(" ")[-1] if pd.notnull(x) else None)
                    df["hora_salida"] = df["hora_salida"].apply(lambda x: str(x).split(" ")[-1] if pd.notnull(x) else None)
                    dataframes.append(df)
                    #ultimo_log_hoja = f"--- Hoja agregada 1: {hoja}, filas: {len(df)} ---"
                    #print(ultimo_log_hoja)

            except ValueError:
                logging.warning(f"🚨 Hoja ignorada (no es fecha válida): {hoja}")
                continue

        if dataframes:
            df_final = pd.concat(dataframes, ignore_index=True)

            # Verificar si hay columnas duplicadas
            duplicates = df_final.columns[df_final.columns.duplicated()]
            if len(duplicates) > 0:
                print("🚨 Columnas duplicadas detectadas:", duplicates.tolist())
            df_final['Ruta_Carpeta'] = Ruta_Carpeta

            print(f"\nTotal filas a subir: {len(df_final)}")
        else:
            logging.warning("No se encontraron hojas válidas.")
            df_final = None

    except FileNotFoundError:
        logging.warning(f"No se encontró el archivo: {archivo_excel}")
        df_final = None

    # Subir a base de datos SQL Server
    if df_final is not None:
        try:
            columnas_ordenadas = [
                    'fecha',
                    'dni',
                    'nombre_completo',
                    'codigo_salesys',
                    'codigo_genesys',
                    'nombre_laraigo',
                    'nombre_360',
                    'codigo_navicat',
                    'codigo_ipcc',
                    'condicion',
                    'cargo',
                    'sub_cargo',
                    'campaña',
                    'estado',
                    'region',
                    'fecha_ingreso_campaña',
                    'hora_entrada',
                    'hora_salida',
                    'supervisor',
                    'asistencia_detalle',
                    'observacion',
                    'Ruta_Carpeta'

            ]

            # Validar que todas existan
            faltantes = [col for col in columnas_ordenadas if col not in df_final.columns]
            if faltantes:
                print(f"⚠️ Columnas faltantes en df_final: {faltantes}")
                return ultimo_log_hoja  # Retornar aunque falten columnas

            # Reordenar columnas
            df_final = df_final[columnas_ordenadas]

            # Conectar y limpiar datos existentes


            # Subir a la tabla
            df_final.to_sql('tblNominaExcelv2', con=engine, if_exists='append', index=False)
            print(f"\n✅ Datos subidos exitosamente a la tabla tblNominaExcelv2")

            # Guardar archivo consolidado

            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\Fotos_Corporativo\{año}\{mesNombre}\Consolidado {mesNombre}.xlsx"

            if os.path.exists(excel_file_path):
                os.remove(excel_file_path)

            df_final.to_excel(excel_file_path, index=False)
            print(f"Datos guardados en el archivo {excel_file_path}.")

        except Exception as e:
            logging.warning(f"\n❌ Error al subir a la base de datos: {e}")
    #return ultimo_log_hoja  # ← Aquí devolvemos el último log
    conexion = conectar_bdStores()
    try:
        
        cursor = conexion.cursor()
        parametros = (año,mes)  # Tupla de tres valores

        # Llamar al procedimiento almacenado
        cursor.callproc('Sp_ActualizacionNomina_Corpo', parametros)

        # Obtener el resultado
        result = cursor.fetchone()
        conexion.commit() 
        print(f"Resultado obtenido: {result}")  # Depuración, muestra el resultado antes de procesar

        if result:  # Si hay resultados
            return result['Total']  # Accede a la clave 'Total' del diccionario
        else:
            return "No Data"  # Si no hay resultados

    except pymssql.DatabaseError as e:
        # Manejo de errores específicos de la base de datos
        logging.warning(f"Error en la base de datos: {e}")
        return f"Error en la base de datos: {e}"

    except Exception as e:
        # Captura de la traza completa del error
        import traceback
        error_details = traceback.format_exc()
        logging.warning(f"Error ocurrió: {error_details}")  # Imprime el error completo
        return f"Error en la obtención de datos: {error_details}"

    finally:
        # Asegurarse de cerrar tanto el cursor como la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()                
        if 'excel' in locals():
                excel.close()
                
def Campaña_Corporativo(fecha_inicio, fecha_fin):
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
    tables = ["TblFotoCorporativoExcel","TblCorporativoAutorizacionesExcel"]

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
        ruta_corpo = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Foto Corporativo\{mesNombre}\FotoCorporativo{dia:02d}.csv"

        if os.path.exists(ruta_corpo):
            try:
                dtype_especifico = {
                    'dnitecn': str
                }
                df_merged_rend = pd.read_csv(ruta_corpo,sep=',',dtype=dtype_especifico)#separador de , en el CSV#
                df_merged_rend.columns = [normalize_column_name(col) for col in df_merged_rend.columns]
                df_merged_rend['hora_inicio_contrata'] = df_merged_rend['hora_inicio_contrata'].apply(parse_fecha) 
                df_merged_rend['hora_inicio_call_center'] = df_merged_rend['hora_inicio_call_center'].apply(parse_fecha) 
                df_merged_rend['hora_fin_call_center'] = df_merged_rend['hora_fin_call_center'].apply(parse_fecha) 

                with engine.connect() as connection:
                    df_merged_rend.to_sql('TblFotoCorporativoExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Alambrico cargado exitosamente para el día {dia}: {ruta_corpo}")
            except Exception as e:
                logging.error(f"Error procesando archivo Alambrico {ruta_corpo} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Alambrico no encontrado para el día {dia}: {ruta_corpo}")

    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_rend_Autorizaciones = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Corporativo Autorizaciones\{mesNombre}\CorporativoAutorizaciones{dia:02d}.xlsx"
        if os.path.exists(ruta_rend_Autorizaciones):
            try:
                df_merged_Autorizaciones = pd.read_excel(ruta_rend_Autorizaciones) #separador de , en el excel# #separador de , en el CSV#
                df_merged_Autorizaciones.columns = [normalize_column_name(col) for col in df_merged_Autorizaciones.columns] 

                df_merged_Autorizaciones['hora_inicio'] = df_merged_Autorizaciones['hora_inicio'].apply(parse_fecha_laraigo) 
                df_merged_Autorizaciones['hora_fin'] = df_merged_Autorizaciones['hora_fin'].apply(parse_fecha_laraigo) 

                with engine.connect() as connection:
                    df_merged_Autorizaciones.to_sql('TblCorporativoAutorizacionesExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Alambrico cargado exitosamente para el día {dia}: {ruta_rend_Autorizaciones}")
            except Exception as e:
                logging.error(f"Error procesando archivo Alambrico {ruta_rend_Autorizaciones} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Alambrico no encontrado para el día {dia}: {ruta_rend_Autorizaciones}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_CampañaCorporativo_rango', parametros)
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

def KpiCorporativo(fecha_fin):
    
    
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

    if isinstance(fecha_fin, str):
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    elif isinstance(fecha_fin, datetime):
        fecha_f = fecha_fin.date()
    elif isinstance(fecha_fin, date):
        fecha_f = fecha_fin
    else:
        raise ValueError("fecha_fin debe ser str, datetime o date")

    hoy = fecha_f
    #ayer= hoy  # Ya es un objeto date
    #mesNombre = hoy.strftime("%B").capitalize()
    mes = hoy.month
    año = hoy.year
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_fin, )
        cursor.callproc('SP_KpiCorporativo', parametros)
        conexion.commit()
        logging.info("Procedimiento almacenado SP_KpiMultiSkill ejecutado correctamente.")
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