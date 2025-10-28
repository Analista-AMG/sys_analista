import pandas as pd
from Campañas.funcion import *
from conexion import *
from unidecode import unidecode
from collections import Counter
from datetime import datetime, date
from deep_translator import GoogleTranslator
from logger_config import session_handler
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

def Campaña_Delivery_Auditoria(fecha_fin):
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
    tables = ["tblDeliveryAuditoriaExcel"]

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
    ruta_Delivery_Auditoria = fr"\\SRV-FS\ReportesDelivery\CAMPAÑA DE AUDITORIA DE ATENCION\{año}\{mesNombre}\Revision_Pedidos_{mesNombre}.xlsx"
    #for dia in range(dia_inicio, dia_fin + 1):

    if os.path.exists(ruta_Delivery_Auditoria):
        try:
            
            df_merged_Delivery_Auditoria = pd.read_excel(ruta_Delivery_Auditoria) #separador de , en el excel#
            df_merged_Delivery_Auditoria.columns = [normalize_column_name(col) for col in df_merged_Delivery_Auditoria.columns]

            df_merged_Delivery_Auditoria['inicio'] = df_merged_Delivery_Auditoria['inicio'].apply(parse_fecha_genesys)
            df_merged_Delivery_Auditoria['fin'] = df_merged_Delivery_Auditoria['fin'].apply(parse_fecha_genesys)
           # df_merged_Delivery_Auditoria['fecha'] = df_merged_Delivery_Auditoria['fecha'].astype(str).str.replace('0/01/1900', '01/01/1900')
            df_merged_Delivery_Auditoria['fecha'] = df_merged_Delivery_Auditoria['fecha'].apply(parse_fecha_genesys)
            df_merged_Delivery_Auditoria['fecha'] = pd.to_datetime(df_merged_Delivery_Auditoria['fecha'], errors='coerce')
            df_merged_Delivery_Auditoria['fecha_amg'] = pd.to_datetime(df_merged_Delivery_Auditoria['fecha_amg'], errors='coerce')
            print(df_merged_Delivery_Auditoria['fecha'].unique())
            df_merged_Delivery_Auditoria['mes'] = mes
            df_merged_Delivery_Auditoria['año'] = año


            columnas_ordenadas = [
            'id',  'pedido',	'base_amg',	'fecha_amg','tipo_de_servicio','proveedor',	'atencion_amg',	'atencion_ol','responsable','observacion','detalle_homologado','ausencia_confirmada','inicio','fin','fecha','codigo_agente','mes','año'
                                ]
            df_merged_Delivery_Auditoria = df_merged_Delivery_Auditoria[columnas_ordenadas]


            with engine.connect() as connection:
                df_merged_Delivery_Auditoria.to_sql('tblDeliveryAuditoriaExcel', con=connection, if_exists='replace', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo DELIVERY cargado exitosamente para el mes {mes}: {ruta_Delivery_Auditoria}")
        except Exception as e:
            logging.error(f"Error procesando archivo DELIVERY {ruta_Delivery_Auditoria} para el día {mes}: {e}")
    else:
        logging.warning(f"Archivo DELIVERY no encontrado para el mes {mes}: {ruta_Delivery_Auditoria}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_f,)
        cursor.callproc('Sp_DeliveryAuditoria_rango', parametros)
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


def Campaña_Delivery(fecha_inicio, fecha_fin):
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

    # Limpia el log existente antes de una nueva ejecución
    open('Campañas.log', 'w', encoding='utf-8').close()
    logging.info(f"Iniciando nueva ejecución para fechas: {fecha_inicio} a {fecha_fin}")
    ################################################################################################
    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_Delivery = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\General\delivery{dia:02d}.csv"
        if os.path.exists(ruta_Delivery):
            try:
                df_Delivery = pd.read_csv(ruta_Delivery, sep=',', encoding='utf-8')
                df_Delivery.columns = [normalize_column_name(col) for col in df_Delivery.columns]
                df_Delivery['nombre_usuario'] = df_Delivery['nombre_usuario'].replace('100722A', '1007220')
                df_Delivery['hora_inicio_contrata'] = pd.to_datetime(df_Delivery['hora_inicio_contrata'], errors='coerce')
                df_Delivery['hora_inicio_call_center'] = pd.to_datetime(df_Delivery['hora_inicio_call_center'], errors='coerce')
                df_Delivery['hora_fin_call_center'] = pd.to_datetime(df_Delivery['hora_fin_call_center'], errors='coerce')

                with engine.connect() as connection:
                    df_Delivery.to_sql('TblDeliveryExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo DELIVERY cargado exitosamente para el día {dia}: {ruta_Delivery}")
            except Exception as e:
                logging.error(f"Error procesando archivo DELIVERY {ruta_Delivery} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo DELIVERY no encontrado para el día {dia}: {ruta_Delivery}")

    ################################################################################################
    # Procesar archivos TOA por día
    for dia in range(dia_inicio, dia_fin + 1):
        fecha_actual = datetime(año, fecha_ini.month, dia)
        mesNombre = fecha_actual.strftime("%B").capitalize()

        rutas = {
            "Logixtal": fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\TOA\Logixtal\actividades_logixtal_{dia:02d}.xlsx",
            "Scharff": fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\TOA\Scharff\actividades_scharff_{dia:02d}.xlsx",
            "Sli": fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\TOA\Sli\actividades_sli_{dia:02d}.xlsx"
        }

        dataframes = []
        for nombre, ruta in rutas.items():
            if os.path.exists(ruta):
                try:
                    df = pd.read_excel(ruta, engine='openpyxl')
                    df.columns = [normalize_column_name(c) for c in df.columns]

                    cols = pd.Series(df.columns)
                    if cols[cols == "zona_de_trabajo"].count() > 1:
                        duplicados = cols[cols == "zona_de_trabajo"].index.tolist()
                        cols[duplicados[1]] = "zona_de_trabajo1"
                        df.columns = cols

                    dataframes.append(df)
                    logging.info(f"Archivo TOA {nombre} cargado para el día {dia}: {ruta}")
                except Exception as e:
                    logging.error(f"Error leyendo TOA {nombre} ({ruta}) para el día {dia}: {e}")
                    dataframes.append(pd.DataFrame())
            else:
                logging.warning(f"Archivo TOA {nombre} no encontrado para el día {dia}: {ruta}")
                dataframes.append(pd.DataFrame())

        dataframes_validos = [df for df in dataframes if not df.empty and not df.isna().all().all()]

        if not dataframes_validos:
            logging.warning(f"Todos los archivos TOA vacíos o inválidos para el día {dia}")
            continue

        try:
            df_toa = pd.concat(dataframes_validos, ignore_index=True)
            columnas_clave = ['fecha_de_programacion', 'sla_inicio', 'sla_fin', 'fecha_de_entrega']

            for col in columnas_clave:
                if col not in df_toa.columns:
                    logging.error(f"Falta columna requerida en TOA: {col} para el día {dia}")
                    return

            df_toa['fecha_de_programacion'] = df_toa['fecha_de_programacion'].apply(parse_fecha_TOA)
            df_toa['sla_inicio'] = df_toa['sla_inicio'].apply(parse_fecha_corpo)
            df_toa['sla_fin'] = df_toa['sla_fin'].apply(parse_fecha_corpo)
            df_toa['fecha_de_entrega'] = df_toa['fecha_de_entrega'].apply(parse_fecha_corpo)

            with engine.connect() as connection:
                df_toa.to_sql('TblClaroToaExcel', con=connection, if_exists='append', index=False)

            logging.info(f"Archivo TOA consolidado cargado para el día {dia}")

        except Exception as e:
            logging.warning(f"Error procesando TOA para el día {dia}: {e}")

    ################################################################################################
    # Consulta a Navicat
    conexion = conectar_bdStores_Intranet()
    cursor_navicat = conexion.cursor()

    query = f"""
        SELECT DISTINCT 
            `nro_pedido`, `nombre_cliente`, `dni_cliente`, `telefono_cliente`, `nombre_motorizado`, `empresa`, `telefono_motorizado`, 
            `tipo_pago`, `id_pago`, `monto_cobrar`, `tipo_tarjeta`, `gestion`, `resultado`, `subresultado`, `observacion`,	
            DATE_FORMAT(`hora_inicio`, '%H:%i:%s') as `hora_inicio`,
            DATE_FORMAT(`hora_fin`, '%H:%i:%s') as `hora_fin`,
            `asesor`, `tmo`,
            DATE_FORMAT(STR_TO_DATE(fecha, '%d/%m/%Y'), '%Y-%m-%d') as fecha
        FROM vista_reporte_ivr 
        WHERE DATE_FORMAT(STR_TO_DATE(fecha, '%d/%m/%Y'), '%Y-%m-%d') BETWEEN '{fecha_ini.strftime('%Y-%m-%d')}' AND '{fecha_f.strftime('%Y-%m-%d')}'
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

def CargaNominaDeliveryBioMensajeriaSoporte(fecha_fin):
    
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
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\Delivery\{año}\{mesNombre}\Delivery_Bio_Mensajeria_Soporte\nomina_{hoy.strftime('%Y%m')}.xlsx"
    Ruta_Carpeta = archivo_excel.split("\\")[7]

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
            print("No se encontraron hojas válidas.")
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

            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\Delivery\{año}\{mesNombre}\Delivery_Bio_Mensajeria_Soporte\Consolidado {mesNombre}.xlsx"

            if os.path.exists(excel_file_path):
                os.remove(excel_file_path)

            df_final.to_excel(excel_file_path, index=False)
            logging.warning(f"Datos guardados en el archivo {excel_file_path}.")

        except Exception as e:
            logging.warning(f"\n❌ Error al subir a la base de datos: {e}")
    #return ultimo_log_hoja  # ← Aquí devolvemos el último log
    conexion = conectar_bdStores()
    try:
        
        cursor = conexion.cursor()
        parametros = (año,mes)  # Tupla de tres valores

        # Llamar al procedimiento almacenado
        cursor.callproc('Sp_ActualizacionNomina_Delivery', parametros)

        # Obtener el resultado
        result = cursor.fetchone()
        conexion.commit() 
        logging.warning(f"Resultado obtenido: {result}")  # Depuración, muestra el resultado antes de procesar

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

def CargaNominaDeliverySeguimiento(fecha_fin):
    
    
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

    # Ruta del archivo Excel
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\Delivery\{año}\{mesNombre}\Delivery_Seguimiento\nomina_{hoy.strftime('%Y%m')}.xlsx"
    Ruta_Carpeta = archivo_excel.split("\\")[7]

    # Lista para guardar los DataFrames
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
                    # ultimo_log_hoja = f"--- Hoja agregada 1: {hoja}, filas: {len(df)} ---"
                    # print(ultimo_log_hoja)

            except ValueError:
                logging.warning(f"Hoja ignorada (no es fecha válida): {hoja}")
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
            print("No se encontraron hojas válidas.")
            df_final = None

    except FileNotFoundError:
        print(f"No se encontró el archivo: {archivo_excel}")
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

            df_final.to_sql('tblNominaExcelv2', con=engine, if_exists='append', index=False)
            print(f"\n✅ Datos subidos exitosamente a la tabla tblNominaExcelv2")

            # Guardar archivo consolidado
            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\Delivery\{año}\{mesNombre}\Delivery_Seguimiento\Consolidado {mesNombre}.xlsx"

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
        cursor.callproc('Sp_ActualizacionNomina_DeliverySeguimiento', parametros)

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

def KpiDelivery(fecha_fin):
    
    
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
        parametros = (año,mes )
        cursor.callproc('SP_KpiDelivery', parametros)
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

############################################################################
## ACA INICIA CARGA POR RANGOS
def Campaña_Delivery_Detallado (fecha_inicio, fecha_fin):
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
    tables = ["TblDeliveryRechazoExcel","TblDeliveryReprogramacionExcel"]

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
        ruta_delivery_rechazo = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\Rechazo\rechazo{dia:02d}.csv"
        ruta_delivery_reprogramacion = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\Reprogramacion\reprogramacion{dia:02d}.csv"

        if os.path.exists(ruta_delivery_rechazo):
            try:
                # SOLUCIÓN: Preprocesar el archivo para unir líneas rotas
                from io import StringIO
                import re
                
                # Leer el archivo completo
                with open(ruta_delivery_rechazo, 'r', encoding='latin1') as f:
                    lineas = f.readlines()
                
                # Obtener el número de columnas del encabezado
                encabezado = lineas[0].strip()
                num_columnas = encabezado.count(',') + 1
                
                lineas_corregidas = [encabezado]
                i = 1
                
                while i < len(lineas):
                    linea_actual = lineas[i].rstrip('\n\r')
                    
                    # Contar el número de campos en la línea actual
                    # Un campo completo termina con comilla antes de la coma o al final
                    count_comillas = linea_actual.count('"')
                    count_comas = linea_actual.count(',')
                    
                    # Si las comillas son impares O el número de campos es menor al esperado
                    # significa que la línea está incompleta
                    while (count_comillas % 2 != 0 or count_comas < num_columnas - 1) and i + 1 < len(lineas):
                        # Unir con la siguiente línea (reemplazando el salto por un espacio)
                        i += 1
                        linea_siguiente = lineas[i].rstrip('\n\r')
                        linea_actual = linea_actual + ' ' + linea_siguiente
                        count_comillas = linea_actual.count('"')
                        count_comas = linea_actual.count(',')
                    
                    # Limpiar comillas internas del campo observacion (penúltimo campo)
                    if '","' in linea_actual:
                        partes = linea_actual.split('","')
                        if len(partes) >= 2:
                            # Limpiar comillas del penúltimo campo
                            partes[-2] = partes[-2].replace('"', '')
                        linea_actual = '","'.join(partes)
                    
                    lineas_corregidas.append(linea_actual)
                    i += 1
                
                # Unir todas las líneas corregidas
                contenido_limpio = '\n'.join(lineas_corregidas)
                
                # Leer con pandas desde el string limpio
                df_rechazo = pd.read_csv(
                    StringIO(contenido_limpio),
                    sep=',',
                    encoding='latin1'#,on_bad_lines='skip'
                )
                df_rechazo.columns = [normalize_column_name(col) for col in df_rechazo.columns]
                
                # Limpieza adicional del campo observacion
                if 'observacion' in df_rechazo.columns:
                    df_rechazo['observacion'] = df_rechazo['observacion'].astype(str).str.replace('"', '', regex=False)
                    df_rechazo['observacion'] = df_rechazo['observacion'].str.replace('\n', ' ', regex=False)
                    df_rechazo['observacion'] = df_rechazo['observacion'].str.replace('\r', ' ', regex=False)
                    df_rechazo['observacion'] = df_rechazo['observacion'].str.strip()
                
                df_rechazo['hora_inicio_contrata'] = pd.to_datetime(df_rechazo['hora_inicio_contrata'], errors='coerce')
                df_rechazo['hora_inicio_call_center'] = pd.to_datetime(df_rechazo['hora_inicio_call_center'], errors='coerce')
                df_rechazo['hora_fin_call_center'] = pd.to_datetime(df_rechazo['hora_fin_call_center'], errors='coerce')

                with engine.connect() as connection:
                    df_rechazo.to_sql('TblDeliveryRechazoExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo DELIVERY cargado exitosamente para el día {dia}: {ruta_delivery_rechazo}")
            except Exception as e:
                logging.error(f"Error procesando archivo DELIVERY {ruta_delivery_rechazo} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo DELIVERY no encontrado para el día {dia}: {ruta_delivery_rechazo}")
            
        if os.path.exists(ruta_delivery_reprogramacion):
            try:
                # SOLUCIÓN: Preprocesar el archivo para unir líneas rotas
                from io import StringIO
                import re
                
                # Leer el archivo completo
                with open(ruta_delivery_reprogramacion, 'r', encoding='latin1') as f:
                    lineas = f.readlines()
                
                # Obtener el número de columnas del encabezado
                encabezado = lineas[0].strip()
                num_columnas = encabezado.count(',') + 1
                
                lineas_corregidas = [encabezado]
                i = 1
                
                while i < len(lineas):
                    linea_actual = lineas[i].rstrip('\n\r')
                    
                    # Contar el número de campos en la línea actual
                    # Un campo completo termina con comilla antes de la coma o al final
                    count_comillas = linea_actual.count('"')
                    count_comas = linea_actual.count(',')
                    
                    # Si las comillas son impares O el número de campos es menor al esperado
                    # significa que la línea está incompleta
                    while (count_comillas % 2 != 0 or count_comas < num_columnas - 1) and i + 1 < len(lineas):
                        # Unir con la siguiente línea (reemplazando el salto por un espacio)
                        i += 1
                        linea_siguiente = lineas[i].rstrip('\n\r')
                        linea_actual = linea_actual + ' ' + linea_siguiente
                        count_comillas = linea_actual.count('"')
                        count_comas = linea_actual.count(',')
                    
                    # Limpiar comillas internas del campo observacion (penúltimo campo)
                    if '","' in linea_actual:
                        partes = linea_actual.split('","')
                        if len(partes) >= 2:
                            # Limpiar comillas del penúltimo campo
                            partes[-2] = partes[-2].replace('"', '')
                        linea_actual = '","'.join(partes)
                    
                    lineas_corregidas.append(linea_actual)
                    i += 1
                
                # Unir todas las líneas corregidas
                contenido_limpio = '\n'.join(lineas_corregidas)
                
                # Leer con pandas desde el string limpio
                df_reprogramacion = pd.read_csv(
                    StringIO(contenido_limpio),
                    sep=',',
                    encoding='latin1'#,on_bad_lines='skip'
                )
                df_reprogramacion.columns = [normalize_column_name(col) for col in df_reprogramacion.columns]
                
                # Limpieza adicional del campo observacion
                if 'observacion' in df_reprogramacion.columns:
                    df_reprogramacion['observacion'] = df_reprogramacion['observacion'].astype(str).str.replace('"', '', regex=False)
                    df_reprogramacion['observacion'] = df_reprogramacion['observacion'].str.replace('\n', ' ', regex=False)
                    df_reprogramacion['observacion'] = df_reprogramacion['observacion'].str.replace('\r', ' ', regex=False)
                    df_reprogramacion['observacion'] = df_reprogramacion['observacion'].str.strip()
                
                df_reprogramacion['hora_inicio_contrata'] = pd.to_datetime(df_reprogramacion['hora_inicio_contrata'], errors='coerce')
                df_reprogramacion['hora_inicio_call_center'] = pd.to_datetime(df_reprogramacion['hora_inicio_call_center'], errors='coerce')
                df_reprogramacion['hora_fin_call_center'] = pd.to_datetime(df_reprogramacion['hora_fin_call_center'], errors='coerce')

                with engine.connect() as connection:
                    df_reprogramacion.to_sql('TblDeliveryReprogramacionExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo DELIVERY cargado exitosamente para el día {dia}: {ruta_delivery_reprogramacion}")
            except Exception as e:
                logging.error(f"Error procesando archivo DELIVERY {ruta_delivery_reprogramacion} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo DELIVERY no encontrado para el día {dia}: {ruta_delivery_reprogramacion}")            

    #############################################################################################
    # conexion = conectar_bdStores()
    # try:
    #     cursor = conexion.cursor()
    #     parametros = (fecha_ini, fecha_f)
    #     cursor.callproc('Sp_Delivery_Detallado_rango', parametros)
    #     conexion.commit()
    #     logging.info("Procedimiento almacenado Sp_Delivery_Detallado ejecutado correctamente.")
    # except Exception as e:
    #     import traceback
    #     error_details = traceback.format_exc()
    #     logging.error(f"Error en la ejecución del procedimiento almacenado: {error_details}")
    #     return f"Error en la obtención de datos: {error_details}"
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if conexion:
    #         conexion.close()












































# ############# ACA INICIA CARGA MENSUAL
# def Campaña_Delivery_Detallado (fecha_fin):

#     try:
#         locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux
#     except locale.Error:
#         try:
#             locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
#         except locale.Error:
#             logging.warning("No se pudo establecer el locale en español. Se usará el predeterminado.")
             
#     engine = conectar_bdCargaExcel()

#     ################################################################################################
#     # Eliminar información de las tablas Excel
#     tables = [
#             "TblDeliveryRechazoExcel",
#             "TblDeliveryReprogramacionExcel"
#     ]

#     with engine.connect() as connection:
#         with connection.begin() as transaction:
#             for table in tables:
#                 connection.execute(text(f"DELETE FROM {table}"))
#                 logging.info(f"Contenido eliminado de la tabla {table}")

#     ################################################################################################
#     # Convertir strings de fechas
#     fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
#     dia_fin = fecha_f.day
#     año = fecha_f.year
#     mes = fecha_f.month
#     mesNombre = fecha_f.strftime("%B").capitalize()

#     # Limpia el log existente antes de una nueva ejecución
#     open('Campañas.log', 'w', encoding='utf-8').close()
#     logging.info(f"Iniciando nueva ejecución del mes de {mesNombre}")
#     ################################################################################################
#     # Procesar archivos delivery por día
#     #for dia in range(dia_inicio, dia_fin + 1):
#     ruta_rechazo_delivery 			= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\rechazo.csv"
#     ruta_repro_delivery				= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Delivery\{mesNombre}\repro.csv"
    
#     df_rechazo_delivery = pd.read_csv(ruta_rechazo_delivery,sep=',',encoding='latin1') 
#     df_repro_delivery   = pd.read_csv(ruta_repro_delivery,sep=',',encoding='latin1')
    
#     df_rechazo_delivery.columns = [normalize_column_name(col) for col in df_rechazo_delivery.columns]
#     df_repro_delivery.columns = [normalize_column_name(col) for col in df_repro_delivery.columns]    

#     #Normalizar fechas  
#     df_rechazo_delivery['hora_inicio_contrata'] = df_rechazo_delivery['hora_inicio_contrata'].apply(parse_fecha) 
#     df_rechazo_delivery['hora_inicio_call_center'] = df_rechazo_delivery['hora_inicio_call_center'].apply(parse_fecha) 
#     df_rechazo_delivery['hora_fin_call_center'] = df_rechazo_delivery['hora_fin_call_center'].apply(parse_fecha)
#     df_repro_delivery['hora_inicio_contrata'] = df_repro_delivery['hora_inicio_contrata'].apply(parse_fecha) 
#     df_repro_delivery['hora_inicio_call_center'] = df_repro_delivery['hora_inicio_call_center'].apply(parse_fecha) 
#     df_repro_delivery['hora_fin_call_center'] = df_repro_delivery['hora_fin_call_center'].apply(parse_fecha) 
    
#     # ##CARGA REPRO
#     with engine.connect() as connection:
#         df_rechazo_delivery.to_sql('TblDeliveryRechazoExcel', con=connection, if_exists='append', index=False)
#         connection.execute(text("COMMIT"))
#     print("Datos cargados exitosamente en la base de datos TblDeliveryRechazoExcel.")
#     #-2-#####################################################################################################################
#     with engine.connect() as connection:
#         df_repro_delivery.to_sql('TblDeliveryReprogramacionExcel', con=connection, if_exists='append', index=False)
#         connection.execute(text("COMMIT"))
#     print("Datos cargados exitosamente en la base de datos TblDeliveryReprogramacionExcel.")

#     #############################################################################################
#     conexion = conectar_bdStores()
#     try:
#         cursor = conexion.cursor()
#         parametros = (año, mes)
#         cursor.callproc('Sp_Delivery_Detallado_rango', parametros)
#         conexion.commit()
#         logging.info("Procedimiento almacenado Sp_Delivery_Detallado ejecutado correctamente.")
#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         logging.error(f"Error en la ejecución del procedimiento almacenado: {error_details}")
#         return f"Error en la obtención de datos: {error_details}"
#     finally:
#         if cursor:
#             cursor.close()
#         if conexion:
#             conexion.close()