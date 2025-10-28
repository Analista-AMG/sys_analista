import pandas as pd
from Campañas.funcion import *
from conexion import *
from unidecode import unidecode
from collections import Counter
from datetime import datetime, date
from deep_translator import GoogleTranslator
import os
import traceback
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

def CargaNominaMultiskill(fecha_fin):
    
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
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\Planta_Externa_Multiskill\{año}\{mesNombre}\nomina_{hoy.strftime('%Y%m')}.xlsx"
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
        print(f"No se encontró el archivo: {archivo_excel}")
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

            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\Planta_Externa_Multiskill\{año}\{mesNombre}\Consolidado {mesNombre}.xlsx"

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
        cursor.callproc('Sp_ActualizacionNomina_Multiskill', parametros)

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
                
def Campaña_Multiskill(fecha_inicio, fecha_fin):
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
    tables = ["TblPlantaExternaExcel"]

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
        ruta_PEX = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Planta Externa\Casos_apk\{mesNombre}\PlantaExterna{dia:02d}.csv"

        if os.path.exists(ruta_PEX):
            try:
                dtype_especifico = {
                    'dni_tecn': str
                }


                df_PEX = pd.read_csv(ruta_PEX, sep=',', encoding='utf-8',dtype=dtype_especifico)
                df_PEX.columns = [normalize_column_name(col) for col in df_PEX.columns]
                df_PEX['hora_inicio_contrata'] = pd.to_datetime(df_PEX['hora_inicio_contrata'])
                df_PEX['hora_inicio_call_center'] = pd.to_datetime(df_PEX['hora_inicio_call_center'])
                df_PEX['hora_fin_call_center'] = pd.to_datetime(df_PEX['hora_fin_call_center'])


                with engine.connect() as connection:
                    df_PEX.to_sql('TblPlantaExternaExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo DELIVERY cargado exitosamente para el día {dia}: {ruta_PEX}")
            except Exception as e:
                logging.error(f"Error procesando archivo DELIVERY {ruta_PEX} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo DELIVERY no encontrado para el día {dia}: {ruta_PEX}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_CampañaPlantaExterna_rango', parametros)
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

def KpiMultiskill(fecha_fin):
    
    
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
        cursor.callproc('SP_KpiMultiSkill', parametros)
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


def TardanzasMultiskill(fecha_inicio,fecha_fin):
    
    
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

    fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini,fecha_f)
        cursor.callproc('Sp_tardanzasMultiSkill', parametros)
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


def Laraigo_Multiskill(fecha_inicio, fecha_fin):
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
    tables = ["TblLaraigoPexExcel"]

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

        ruta_Laraigo = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Laraigo\PEX\{mesNombre}\Laraigo{dia:02d}.csv"

        if os.path.exists(ruta_Laraigo):
            try:

                #df_merged_Laraigo = pd.read_csv(ruta_Laraigo, sep='|', encoding='latin1', errors='replace')
                df_merged_Laraigo = pd.read_csv(ruta_Laraigo,sep='|',encoding="latin1") #separador de , en el CSV#

                df_merged_Laraigo.columns = [normalize_column_name(col) for col in df_merged_Laraigo.columns]
                df_merged_Laraigo['fecha_de_inicio'] = df_merged_Laraigo['fecha_de_inicio'].apply(parse_fecha_laraigo)
                df_merged_Laraigo['fecha_de_fin'] = df_merged_Laraigo['fecha_de_fin'].apply(parse_fecha_laraigo)
                df_merged_Laraigo['fecha_de_derivacion'] = df_merged_Laraigo['fecha_de_derivacion'].apply(parse_fecha_laraigo)
                df_merged_Laraigo['fecha_de_publicacion_original'] = df_merged_Laraigo['fecha_de_publicacion_original'].apply(parse_fecha_laraigo)
                df_merged_Laraigo['fecha_de_ultima_interaccion'] = df_merged_Laraigo['fecha_de_ultima_interaccion'].apply(parse_fecha_laraigo)


                with engine.connect() as connection:
                    df_merged_Laraigo.to_sql('TblLaraigoPexExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo DELIVERY cargado exitosamente para el día {dia}: {ruta_Laraigo}")
            except Exception as e:
                logging.error(f"Error procesando archivo DELIVERY {ruta_Laraigo} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo DELIVERY no encontrado para el día {dia}: {ruta_Laraigo}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_CampañaLaraigoPex_rango', parametros)
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


def Interacciones_Multiskill(fecha_inicio, fecha_fin):
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
    with engine.connect() as connection:
            # Iniciar una transacción explícita
        with connection.begin() as transaction:
            connection.execute(text(f"DELETE FROM TblInteraccionesExcel where (cola LIKE '%MULTISKILL%')"))
            transaction.commit()

    with engine.connect() as connection:
            # Iniciar una transacción explícita
        with connection.begin() as transaction:
            connection.execute(text(f"DELETE FROM TblInteraccionesExcel where exportacion_completa_finalizada is null"  ))
            transaction.commit()

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
        ruta_InteraccionesMultiskill = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Planta Externa\Interacciones\{mesNombre}\interacciones{dia:02d}.csv"

        if os.path.exists(ruta_InteraccionesMultiskill):
            try:
                
                df_merged_Interacciones_Multi = pd.read_csv(ruta_InteraccionesMultiskill,sep=',')
                df_merged_Interacciones_Multi.columns = [normalize_column_name(col) for col in df_merged_Interacciones_Multi.columns]
                df_merged_Interacciones_Multi['fecha'] = df_merged_Interacciones_Multi['fecha'].apply(parse_fecha_genesys)

                with engine.begin() as connection:  # Esto asegura commit automático si no hay error
                    df_merged_Interacciones_Multi.to_sql('TblInteraccionesExcel', con=connection, if_exists='append', index=False)

                logging.info(f"Archivo Interacciones cargado exitosamente para el día {dia}: {ruta_InteraccionesMultiskill}")
            except Exception as e:
                logging.error(f"Error procesando archivo Interacciones {ruta_InteraccionesMultiskill} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Interacciones no encontrado para el día {dia}: {ruta_InteraccionesMultiskill}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('sp_InteraccionesDeliveryPEX_rango', parametros)
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


def Campaña_Multiskill_Navicat(fecha_inicio, fecha_fin):
    # Configurar logging en una ruta segura del servidor
    try:
        logging.basicConfig(
            filename='/tmp/Campañas.log',
            level=logging.INFO,
            encoding='utf-8',
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    except Exception as e:
        print("⚠️ No se pudo inicializar el log correctamente.")
        print(e)

    try:
        # Configurar locale en español si está disponible
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
            except locale.Error:
                logging.warning("No se pudo establecer el locale en español. Se usará el predeterminado.")

        # Conversión de fechas
        fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
        mesNombre = fecha_f.strftime("%B").capitalize()

        logging.info(f"🔄 Ejecutando campaña para fechas: {fecha_inicio} a {fecha_fin}")
        print(f"🔄 Ejecutando campaña para fechas: {fecha_inicio} a {fecha_fin}")

        # Conexión a base de datos de destino
        engine = conectar_bdCargaExcel()

        # Eliminar registros existentes
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(
                    text("""
                        DELETE FROM tblRegistrosObservadosMultiskill
                        WHERE fecha >= :inicio AND fecha <= :fin
                    """),
                    {"inicio": fecha_ini.strftime('%Y-%m-%d'), "fin": fecha_f.strftime('%Y-%m-%d')}
                )
                logging.info("🧹 Registros anteriores eliminados.")
                print("🧹 Registros anteriores eliminados.")

        # Conexión a Navicat
        conexion = conectar_bdStores_MultiSkill()
        cursor = conexion.cursor()

        # Consulta SQL
        query = f"""
                select *      
                FROM Supervision_Campo_AMG
                WHERE Fecha >= '{fecha_ini.strftime('%Y-%m-%d')}'
                AND Fecha <= '{fecha_f.strftime('%Y-%m-%d')}'
        """
        cursor.execute(query)
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        if not datos:
            msg = "⚠️ No se encontraron datos en ese rango de fechas."
            logging.warning(msg)
            print(msg)
            return

        df = pd.DataFrame(datos, columns=columnas)

        # Normalizar nombres de columnas (debes definir esta función)
        df.columns = [normalize_column_name(col) for col in df.columns]

        # Inserción en bloques
        motor = conectar_bdCargaExcel()
        df.to_sql(
            'tblRegistrosObservadosMultiskill',
            motor,
            if_exists='append',
            index=False,
            chunksize=5000
        )

        msg = f"✅ {len(df)} registros cargados exitosamente."
        logging.info(msg)
        print(msg)

    except Exception:
        error_trace = traceback.format_exc()

        # Imprimir el error en consola
        print("❌ Error inesperado al ejecutar el reporte.")
        print(error_trace)

        # Guardar el error en log
        try:
            logging.error("❌ Error inesperado al ejecutar el reporte:")
            logging.error(error_trace)
        except Exception as log_error:
            print("⚠️ Además, hubo un problema al escribir en el log:")
            print(log_error)


def Validacionestickets(fecha_inicio,fecha_fin):
    
    
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

    fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini,fecha_f )
        cursor.callproc('sp_ValidacionLaraigoTicket', parametros)
        conexion.commit()
        logging.info("Procedimiento almacenado sp_ValidacionLaraigoTicket ejecutado correctamente.")
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



def Campaña_Multiskill_Navicat_2(fecha_inicio, fecha_fin):
    # Configurar logging en una ruta segura del servidor
    try:
        logging.basicConfig(
            filename='/tmp/Campañas.log',
            level=logging.INFO,
            encoding='utf-8',
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    except Exception as e:
        print("⚠️ No se pudo inicializar el log correctamente.")
        print(e)

    try:
        # Configurar locale en español si está disponible
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
            except locale.Error:
                logging.warning("No se pudo establecer el locale en español. Se usará el predeterminado.")

        # Conversión de fechas
        fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
        mesNombre = fecha_f.strftime("%B").capitalize()

        logging.info(f"🔄 Ejecutando campaña para fechas: {fecha_inicio} a {fecha_fin}")
        print(f"🔄 Ejecutando campaña para fechas: {fecha_inicio} a {fecha_fin}")

        # Conexión a base de datos de destino
        engine = conectar_bdCargaExcel()

        # Eliminar registros existentes
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(
                    text("""
                        DELETE FROM Tbl_Registros_2N_Multiskill
                        WHERE fecha >= :inicio AND fecha <= :fin
                    """),
                    {"inicio": fecha_ini.strftime('%Y-%m-%d'), "fin": fecha_f.strftime('%Y-%m-%d')}
                )
                logging.info("🧹 Registros anteriores eliminados.")
                print("🧹 Registros anteriores eliminados.")

        # Conexión a Navicat
        conexion = conectar_bdStores_MultiSkill()
        cursor = conexion.cursor()

        # Consulta SQL
        query = f"""
                SELECT 
                `Fecha`,
                DATE_FORMAT(`Hora_inicio`, '%H:%i:%s') AS Hora_inicio,
                DATE_FORMAT(`Hora_fin`, '%H:%i:%s')   AS Hora_fin,
                `SOT`,
                `CONTRATA_REPORTE`,
                `DNI`,
                `RPC_tecnico`,
                `Técnico`,
                `Tipo_de_actividad`,
                `Asesor`,
                `Reporto_inicio`,
                `Solicita_soporte`,
                `Departamento`,
                `Región`,
                `Envio_foto_prob_sol`,
                `Comentario_adicional`
                FROM `2N_Registro _actividad`
                WHERE Fecha >= '{fecha_ini.strftime('%Y-%m-%d')}'
                AND Fecha <= '{fecha_f.strftime('%Y-%m-%d')}'
        """
        cursor.execute(query)
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        if not datos:
            msg = "⚠️ No se encontraron datos en ese rango de fechas."
            logging.warning(msg)
            print(msg)
            return

        df = pd.DataFrame(datos, columns=columnas)

        # Normalizar nombres de columnas (debes definir esta función)
        df.columns = [normalize_column_name(col) for col in df.columns]


        # Inserción en bloques
        motor = conectar_bdCargaExcel()
        df.to_sql(
            'Tbl_Registros_2N_Multiskill',
            motor,
            if_exists='append',
            index=False,
            chunksize=5000
        )

        msg = f"✅ {len(df)} registros cargados exitosamente."
        logging.info(msg)
        print(msg)

    except Exception:
        error_trace = traceback.format_exc()

        # Imprimir el error en consola
        print("❌ Error inesperado al ejecutar el reporte.")
        print(error_trace)

        # Guardar el error en log
        try:
            logging.error("❌ Error inesperado al ejecutar el reporte:")
            logging.error(error_trace)
        except Exception as log_error:
            print("⚠️ Además, hubo un problema al escribir en el log:")
            print(log_error)

def Campaña_Multiskill_Navicat_3(fecha_inicio, fecha_fin):
    # Configurar logging en una ruta segura del servidor
    try:
        logging.basicConfig(
            filename='/tmp/Campañas.log',
            level=logging.INFO,
            encoding='utf-8',
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    except Exception as e:
        print("⚠️ No se pudo inicializar el log correctamente.")
        print(e)

    try:
        # Configurar locale en español si está disponible
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
            except locale.Error:
                logging.warning("No se pudo establecer el locale en español. Se usará el predeterminado.")

        # Conversión de fechas
        fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
        mesNombre = fecha_f.strftime("%B").capitalize()

        logging.info(f"🔄 Ejecutando campaña para fechas: {fecha_inicio} a {fecha_fin}")
        print(f"🔄 Ejecutando campaña para fechas: {fecha_inicio} a {fecha_fin}")

        # Conexión a base de datos de destino
        engine = conectar_bdCargaExcel()

        # Eliminar registros existentes
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(
                    text("""
                        DELETE FROM Tbl_Registros_Seguimiento2N
                        WHERE FECHA_DE_REGISTRO >= :inicio AND FECHA_DE_REGISTRO <= :fin
                    """),
                    {"inicio": fecha_ini.strftime('%Y-%m-%d'), "fin": fecha_f.strftime('%Y-%m-%d')}
                )
                logging.info("🧹 Registros anteriores eliminados.")
                print("🧹 Registros anteriores eliminados.")

        # Conexión a Navicat
        conexion = conectar_bdStores_MultiSkill()
        cursor = conexion.cursor()

        # Consulta SQL
        query = f"""
                SELECT 
                    `FECHA_DE_REGISTRO`,
                    `ASESOR`,
                    `ESTADO`,
                    `SOT1`,
                    `CONTRATA`,
                    `PLANO`,
                    `DISTRITO`,
                    `CUSTOMER`,
                    `DEPARTAMENTO`,
                    `TIPO_DE_TRABAJO`,
                    `FECHA_DERIVACION_2N`,
                    `CMTS_OLT`,
                    `SERVICIO`,
                    `TIPO_DE_AVERIA`,
                    `OBSERVACION`,
                    `REMEDY`,
                    `DILACION`,
                    `MESA_DE_ESCALAMIENTO`,
                    `ESTADO_SGA`
                FROM SEGUIMIENTO_CASOS_ESCALADOS_2N
                WHERE DATE(`FECHA_DE_REGISTRO`) >= '{fecha_ini.strftime('%Y-%m-%d')}'
                AND DATE(`FECHA_DE_REGISTRO`) <= '{fecha_f.strftime('%Y-%m-%d')}'
        """
        cursor.execute(query)
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        if not datos:
            msg = "⚠️ No se encontraron datos en ese rango de fechas."
            logging.warning(msg)
            print(msg)
            return

        df = pd.DataFrame(datos, columns=columnas)

        # Normalizar nombres de columnas (debes definir esta función)
        df.columns = [normalize_column_name(col) for col in df.columns]


        # Inserción en bloques
        motor = conectar_bdCargaExcel()
        df.to_sql(
            'Tbl_Registros_Seguimiento2N',
            motor,
            if_exists='append',
            index=False,
            chunksize=5000
        )

        msg = f"✅ {len(df)} registros cargados exitosamente."
        logging.info(msg)
        print(msg)

    except Exception:
        error_trace = traceback.format_exc()

        # Imprimir el error en consola
        print("❌ Error inesperado al ejecutar el reporte.")
        print(error_trace)

        # Guardar el error en log
        try:
            logging.error("❌ Error inesperado al ejecutar el reporte:")
            logging.error(error_trace)
        except Exception as log_error:
            print("⚠️ Además, hubo un problema al escribir en el log:")
            print(log_error)

