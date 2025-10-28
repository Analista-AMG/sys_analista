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

def CargaNominaSVFF(fecha_fin):
    
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
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\\Soporte_Venta_Fibra_Fija\{año}\{mesNombre}\nomina_{hoy.strftime('%Y%m')}.xlsx"
    Ruta_Carpeta = archivo_excel.split("\\")[5]

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
            # Ordenar columnas antes de subir
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

            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\\Soporte_Venta_Fibra_Fija\{año}\{mesNombre}\Consolidado {mesNombre}.xlsx"

            if os.path.exists(excel_file_path):
                os.remove(excel_file_path)

            df_final.to_excel(excel_file_path, index=False)
            print(f"Datos guardados en el archivo {excel_file_path}.")

        except Exception as e:
            print(f"\n❌ Error al subir a la base de datos: {e}")
    #return ultimo_log_hoja  # ← Aquí devolvemos el último log
    conexion = conectar_bdStores()
    try:
        
        cursor = conexion.cursor()
        parametros = (año,mes)  # Tupla de tres valores

        # Llamar al procedimiento almacenado
        cursor.callproc('[Sp_ActualizacionNomina_SoporteVff]', parametros)

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


def Campaña_SVFF_Navicat(fecha_fin):
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
    tables = ["Tbl_SLA_FibraExcel","Tbl_SLA_FijaExcel","Tbl_SLA_DemoExcel"]

    with engine.connect() as connection:
        with connection.begin() as transaction:
            for table in tables:
                connection.execute(text(f"DELETE FROM {table}"))
                logging.info(f"Contenido eliminado de la tabla {table}")

    ################################################################################################
    # Convertir strings de fechas

    fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
    año = fecha_f.year
    mes = fecha_f.month
    mesNombre = fecha_f.strftime("%B").capitalize()

    # Limpia el log existente antes de una nueva ejecución
    open('Campañas.log', 'w', encoding='utf-8').close()
    logging.info(f"Iniciando nueva ejecución para el mes de: {mesNombre}")
    ################################################################################################
    # Procesar archivos delivery por día
    ruta_Demo_SVFF = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Soporte Venta Fibra Fija\{mesNombre}\Correciones\soporte_demo\reporte_demo.xlsx"
    ruta_soporte_fibra_SVFF = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Soporte Venta Fibra Fija\{mesNombre}\Correciones\soporte_fibra\reporte_fibra.xlsx"
    ruta_soporte_fija_SVFF = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Soporte Venta Fibra Fija\{mesNombre}\Correciones\soporte_fija\reporte_fija.xlsx"

    #for dia in range(dia_inicio, dia_fin + 1):
######## Demo #########
    if os.path.exists(ruta_Demo_SVFF):
        try:
            
            #columnas = [desc[0] for desc in ruta_Demo_SVFF.description]

            df__demo_navicat = pd.read_excel(ruta_Demo_SVFF) #separador de , en el excel#
            df__demo_navicat = pd.read_excel(ruta_Demo_SVFF, dtype={'proyecto': str})
            df__demo_navicat.columns = [normalize_column_name(col) for col in df__demo_navicat.columns]
            df__demo_navicat['fecha_recepcion'] = pd.to_datetime(df__demo_navicat['fecha_recepcion'], format='%d/%m/%Y')
            df__demo_navicat['fecha_respuesta'] = pd.to_datetime(df__demo_navicat['fecha_respuesta'], format='%d/%m/%Y')
            df__demo_navicat['fecha_inicio'] = pd.to_datetime(df__demo_navicat['fecha_inicio'], format='%d/%m/%Y')
            df__demo_navicat['fecha_fin'] = pd.to_datetime(df__demo_navicat['fecha_fin'], format='%d/%m/%Y')



            with engine.connect() as connection:
                df__demo_navicat.to_sql('Tbl_SLA_DemoExcel', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo DELIVERY cargado exitosamente para el mes {mes}: {ruta_Demo_SVFF}")
        except Exception as e:
            logging.error(f"Error procesando archivo DELIVERY {ruta_Demo_SVFF} para el día {mes}: {e}")
    else:
        logging.warning(f"Archivo Demo no encontrado para el mes {mes}: {ruta_Demo_SVFF}")

######## Fibra #########
    if os.path.exists(ruta_soporte_fibra_SVFF):
        try:
            
            #columnas = [desc[0] for desc in ruta_Demo_SVFF.description]

            df_soporte_fibra_navicat = pd.read_excel(ruta_soporte_fibra_SVFF) #separador de , en el excel#
            df_soporte_fibra_navicat.columns = [normalize_column_name(col) for col in df_soporte_fibra_navicat.columns]
            df_soporte_fibra_navicat = pd.read_excel(ruta_soporte_fibra_SVFF, dtype={'proyecto': str})
            df_soporte_fibra_navicat['fecha_recepcion'] = pd.to_datetime(df_soporte_fibra_navicat['fecha_recepcion'], format='%d/%m/%Y')
            df_soporte_fibra_navicat['fecha_respuesta'] = pd.to_datetime(df_soporte_fibra_navicat['fecha_respuesta'], format='%d/%m/%Y')
            df_soporte_fibra_navicat['fecha_inicio'] = pd.to_datetime(df_soporte_fibra_navicat['fecha_inicio'], format='%d/%m/%Y')
            df_soporte_fibra_navicat['fecha_fin'] = pd.to_datetime(df_soporte_fibra_navicat['fecha_fin'], format='%d/%m/%Y')



            with engine.connect() as connection:
                df_soporte_fibra_navicat.to_sql('Tbl_SLA_FibraExcel', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo SVFF FIBRA cargado exitosamente para el mes {mes}: {ruta_soporte_fibra_SVFF}")
        except Exception as e:
            logging.error(f"Error procesando archivo Fibra {ruta_soporte_fibra_SVFF} para el día {mes}: {e}")
    else:
        logging.warning(f"Archivo SVFF FIBRA no encontrado para el mes {mes}: {ruta_soporte_fibra_SVFF}")

######## Fija  #########
    if os.path.exists(ruta_soporte_fija_SVFF):
        try:
            
            #columnas = [desc[0] for desc in ruta_Demo_SVFF.description]

            df_soporte_fija_navicat = pd.read_excel(ruta_soporte_fija_SVFF) #separador de , en el excel#
            df_soporte_fija_navicat.columns = [normalize_column_name(col) for col in df_soporte_fija_navicat.columns]
            df_soporte_fija_navicat = pd.read_excel(ruta_soporte_fija_SVFF, dtype={'proyecto': str})
            df_soporte_fija_navicat['fecha_recepcion'] = pd.to_datetime(df_soporte_fija_navicat['fecha_recepcion'], format='%d/%m/%Y')
            df_soporte_fija_navicat['fecha_respuesta'] = pd.to_datetime(df_soporte_fija_navicat['fecha_respuesta'], format='%d/%m/%Y')
            df_soporte_fija_navicat['fecha_inicio'] = pd.to_datetime(df_soporte_fija_navicat['fecha_inicio'], format='%d/%m/%Y')
            df_soporte_fija_navicat['fecha_fin'] = pd.to_datetime(df_soporte_fija_navicat['fecha_fin'], format='%d/%m/%Y')

            with engine.connect() as connection:
                df_soporte_fija_navicat.to_sql('Tbl_SLA_FijaExcel', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo SVFF FIBRA cargado exitosamente para el mes {mes}: {ruta_soporte_fija_SVFF}")
        except Exception as e:
            logging.error(f"Error procesando archivo Fibra {ruta_soporte_fija_SVFF} para el día {mes}: {e}")
    else:
        logging.warning(f"Archivo SVFF FIBRA no encontrado para el mes {mes}: {ruta_soporte_fija_SVFF}")



    #############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_f,)
        cursor.callproc('sp_CampañaSVFF')
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