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

def CargaNominaValidacion(fecha_fin):
    
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
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\Validaciones\{año}\{mesNombre}\nomina_{hoy.strftime('%Y%m')}.xlsx"
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

            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\Validaciones\{año}\{mesNombre}\Consolidado {mesNombre}.xlsx"

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
        cursor.callproc('Sp_ActualizacionNomina_ValidacionRF', parametros)

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

def Campaña_Validaciones(fecha_inicio, fecha_fin):
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
    tables = ["tblReporteGeneral2Excel", "tbldp01FtthExcel", "TblEncuestaExcel"]

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
        ruta_ReporteGeneral = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\Reporte General\{mesNombre}\RGA{dia:02d}.csv"

        if os.path.exists(ruta_ReporteGeneral):
            try:
                
                df_merged_ReporteGeneral = pd.read_csv(ruta_ReporteGeneral, sep=',', encoding='latin1')
                df_merged_ReporteGeneral.columns = [normalize_column_name(col) for col in df_merged_ReporteGeneral.columns]
                def convertir_columnas_fecha(df, columnas):
                    for col in columnas:
                        if col in df.columns:
                            df[col] = pd.to_datetime(df[col], errors='coerce').apply(parse_fecha_Activaciones)
                    return df
                columnas_fecha = ['hora_inicio_contrata', 'hora_inicio_call_center', 'hora_fin_call_center']
                df_merged_ReporteGeneral = convertir_columnas_fecha(df_merged_ReporteGeneral, columnas_fecha)


                with engine.connect() as connection:
                    df_merged_ReporteGeneral.to_sql('tblReporteGeneral2Excel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Valiaciones cargado exitosamente para el día {dia}: {ruta_ReporteGeneral}")
            except Exception as e:
                logging.error(f"Error procesando archivo Valiaciones {ruta_ReporteGeneral} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Valiaciones no encontrado para el día {dia}: {ruta_ReporteGeneral}")
################################################################################################
    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_dp01Ftth = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\Reportes Detallado DP\FTTH\DP01\{mesNombre}\DP{dia:02d}.csv"

        if os.path.exists(ruta_dp01Ftth):
            try:
                df_merged_dp01Ftth = pd.read_csv(ruta_dp01Ftth, sep=',', encoding='latin1')
                df_merged_dp01Ftth.columns = [normalize_column_name_point(normalize_column_name(col)) for col in df_merged_dp01Ftth.columns]

                def convertir_columnas_fecha(df, columnas):
                    for col in columnas:
                        if col in df.columns:
                            df[col] = pd.to_datetime(df[col], errors='coerce').apply(parse_fecha_Activaciones)
                    return df
                columnas_fecha = ['hora_inicio_contrata', 'hora_inicio_call_center', 'hora_fin_call_center']
                df_merged_dp01Ftth = convertir_columnas_fecha(df_merged_dp01Ftth, columnas_fecha)


                with engine.connect() as connection:
                    df_merged_dp01Ftth.to_sql('tbldp01FtthExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Valiaciones cargado exitosamente para el día {dia}: {ruta_dp01Ftth}")
            except Exception as e:
                logging.error(f"Error procesando archivo Valiaciones {ruta_dp01Ftth} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Valiaciones no encontrado para el día {dia}: {ruta_dp01Ftth}")

    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_Encuesta = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\Reportes Detallado DP\FTTH\ENCUESTA\{mesNombre}\Encuesta{dia:02d}.csv"

        if os.path.exists(ruta_Encuesta):
            try:
                df_merged_Encuesta = pd.read_csv(ruta_Encuesta, sep=',', encoding='latin1')
                df_merged_Encuesta.columns = [normalize_column_name(col) for col in df_merged_Encuesta.columns]


                def convertir_columnas_fecha(df, columnas):
                    for col in columnas:
                        if col in df.columns:
                            df[col] = pd.to_datetime(df[col], errors='coerce').apply(parse_fecha_Activaciones)
                    return df
                columnas_fecha = ['hora_inicio_contrata', 'hora_inicio_call_center', 'hora_fin_call_center']
                df_merged_Encuesta = convertir_columnas_fecha(df_merged_Encuesta, columnas_fecha)


                with engine.connect() as connection:
                    df_merged_Encuesta.to_sql('TblEncuestaExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Valiaciones cargado exitosamente para el día {dia}: {ruta_Encuesta}")
            except Exception as e:
                logging.error(f"Error procesando archivo Valiaciones {ruta_Encuesta} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Valiaciones no encontrado para el día {dia}: {ruta_Encuesta}")
####################################################################################################################################################################################
    # Procesar archivos delivery por día
    ruta_bitacora = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\BITACORA INCIDENCIAS\Bitacora Validacion Integrada.xlsx"

    if os.path.exists(ruta_bitacora):
        try:
            df_merged_bitacora = pd.read_excel(ruta_bitacora, sheet_name='BITÁCORA')
            df_merged_bitacora.columns = [normalize_column_name(col) for col in df_merged_bitacora.columns]
            df_merged_bitacora.rename(columns={
            'h.inicio': 'hinicio',
            'h._fin': 'h_fin',
            'f._fin': 'f_fin',
            'f._inicio':'f_inicio'
            

                    }, inplace=True)
            
            with engine.connect() as connection:
                df_merged_bitacora.to_sql('TblBitacoraValidaciones', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo ventas cargado exitosamente para el día {dia}: {ruta_bitacora}")
        except Exception as e:
            logging.error(f"Error procesando archivo ventas {ruta_bitacora} para el día {dia}: {e}")
    else:
        logging.warning(f"Archivo Ventas no encontrado para el mes {mesNombre}: {ruta_bitacora}")


    ###############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_CampañaValidaciones_rango', parametros)
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

def Interacciones_Validaciones(fecha_inicio, fecha_fin):
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
            connection.execute(text(f"DELETE FROM TblInteraccionesExcel where cola LIKE '%VALIDACIONES%'"  ))
            transaction.commit()

    with engine.connect() as connection:
        # Iniciar una transacción explícita
        with connection.begin() as transaction:
            connection.execute(text(f"DELETE FROM TblInteraccionesExcel where  exportacion_completa_finalizada is null"  ))
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
        ruta_interacciones_Validaciones = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\INTERACCIONES\{mesNombre}\interacciones{dia:02d}.csv"

        if os.path.exists(ruta_interacciones_Validaciones):
            try:
                
                df_merged_Interacciones_Validaciones = pd.read_csv(ruta_interacciones_Validaciones,sep=',')
                df_merged_Interacciones_Validaciones.columns = [normalize_column_name(col) for col in df_merged_Interacciones_Validaciones.columns]
                df_merged_Interacciones_Validaciones['fecha'].head
                df_merged_Interacciones_Validaciones['fecha'] = df_merged_Interacciones_Validaciones['fecha'].apply(parse_fecha_genesys)

                with engine.begin() as connection:  # Esto asegura commit automático si no hay error
                    df_merged_Interacciones_Validaciones.to_sql('TblInteraccionesExcel', con=connection, if_exists='append', index=False)

                logging.info(f"Archivo Interacciones cargado exitosamente para el día {dia}: {ruta_interacciones_Validaciones}")
            except Exception as e:
                logging.error(f"Error procesando archivo Interacciones {ruta_interacciones_Validaciones} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Interacciones no encontrado para el día {dia}: {ruta_interacciones_Validaciones}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('sp_InteraccionesValidaciones_rango', parametros)
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

def Campaña_Validaciones_otros(fecha_inicio, fecha_fin):
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
    tables = ["TblBitacoraValidaciones","TblGestionBoFotosExcel","tblValidacionRemotaExcel"]

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

    with engine.connect() as connection:
        # Iniciar una transacción explícita
        with connection.begin() as transaction:
            connection.execute(text(f"DELETE FROM TblDimensionamientoRFBD where convert(date,fecha_actualizacion)='{fecha_f}'"  ))
            transaction.commit()

    # Limpia el log existente antes de una nueva ejecución
    open('Campañas.log', 'w', encoding='utf-8').close()
    logging.info(f"Iniciando nueva ejecución para fechas: {fecha_inicio} a {fecha_fin}")
####################################################################################################################################################################################
    # Procesar archivos delivery por día
    ruta_bitacora = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\BITACORA INCIDENCIAS\Bitacora Validacion Integrada.xlsx"
    if os.path.exists(ruta_bitacora):
        try:
            df_merged_bitacora = pd.read_excel(ruta_bitacora, sheet_name='BITÁCORA')
            df_merged_bitacora.columns = [normalize_column_name(col) for col in df_merged_bitacora.columns]
            df_merged_bitacora.rename(columns={
            'h.inicio': 'hinicio',
            'h._fin': 'h_fin',
            'f._fin': 'f_fin',
            'f._inicio':'f_inicio'
                    }, inplace=True)
            
            with engine.connect() as connection:
                df_merged_bitacora.to_sql('TblBitacoraValidaciones', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo ventas cargado exitosamente para el año {año}: {ruta_bitacora}")
        except Exception as e:
            logging.error(f"Error procesando archivo ventas {ruta_bitacora} para el año {año}: {e}")
    else:
        logging.warning(f"Archivo Ventas no encontrado para el mes {mesNombre}: {ruta_bitacora}")
    ################################################################################################
    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_gestionbo = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\GestionBO\{mesNombre}\GestionBO{dia:02d}.xlsx"

        if os.path.exists(ruta_gestionbo):
            try:
                
                df_merged_gestionbo = pd.read_excel(ruta_gestionbo)
                df_merged_gestionbo.columns = [normalize_column_name(col) for col in df_merged_gestionbo.columns]
                df_merged_gestionbo['fecha_base'] = pd.to_datetime(df_merged_gestionbo['fecha_base'],format='%d/%m/%Y')
                df_merged_gestionbo['fecha_inicio'] = pd.to_datetime(df_merged_gestionbo['fecha_inicio'],format='%d/%m/%Y %H:%M:%S')
                df_merged_gestionbo['fecha_fin'] = pd.to_datetime(df_merged_gestionbo['fecha_fin'],format='%d/%m/%Y %H:%M:%S')

                with engine.connect() as connection:
                    df_merged_gestionbo.to_sql('TblGestionBoFotosExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo GestionBo cargado exitosamente para el día {dia}: {ruta_gestionbo}")
            except Exception as e:
                logging.error(f"Error procesando archivo GestionBo {ruta_gestionbo} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo GestionBo no encontrado para el día {dia}: {ruta_gestionbo}")
################################################################################################
    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_ValidacionRemota = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\Validacion Remota\{mesNombre}\ValidacionRemota{dia:02d}.xlsx"

        if os.path.exists(ruta_ValidacionRemota):
            try:
                
                df_merged_ValidacionRemota = pd.read_excel(ruta_ValidacionRemota)
                df_merged_ValidacionRemota.columns = [normalize_column_name(col) for col in df_merged_ValidacionRemota.columns]
                df_merged_ValidacionRemota['fecha_inicio'] = pd.to_datetime(df_merged_ValidacionRemota['fecha_inicio'],format='%d/%m/%Y %H:%M:%S')
                df_merged_ValidacionRemota['fecha_fin'] = pd.to_datetime(df_merged_ValidacionRemota['fecha_fin'],format='%d/%m/%Y %H:%M:%S')



                with engine.connect() as connection:
                    df_merged_ValidacionRemota.to_sql('tblValidacionRemotaExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Remota cargado exitosamente para el día {dia}: {ruta_ValidacionRemota}")
            except Exception as e:
                logging.error(f"Error procesando archivo Remota {ruta_ValidacionRemota} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Remota no encontrado para el día {dia}: {ruta_ValidacionRemota}")


    
################################################################################################
    # Procesar archivos delivery por día
    ruta_rend_Dimensionado = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Validaciones\Dimensionado\{mesNombre}\dimensionado.xlsx"
    if os.path.exists(ruta_rend_Dimensionado):
        try:
            
            df_merged_Dimensionado = pd.read_excel(ruta_rend_Dimensionado)
            df_merged_Dimensionado['fecha_actualizacion'] = fecha_ini
            df_merged_Dimensionado['fecha_actualizacion'] = pd.to_datetime(df_merged_Dimensionado['fecha_actualizacion'])


            with engine.connect() as connection:
                df_merged_Dimensionado.to_sql('TblDimensionamientoRFBD', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo DELIVERY cargado exitosamente para el mes {mes}: {ruta_rend_Dimensionado}")
        except Exception as e:
            logging.error(f"Error procesando archivo DELIVERY {ruta_rend_Dimensionado} para el día {mes}: {e}")
    else:
        logging.warning(f"Archivo DELIVERY no encontrado para el mes {mes}: {ruta_rend_Dimensionado}")

###############################################################################################

    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_ValidacionesOtros_rango', parametros)
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

def KpiValidaciones(fecha_fin):
    
    
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
        cursor.callproc('SP_KpiValidaciones', parametros)
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

def Validacion_Remota_navicat(fecha_inicio, fecha_fin):
    try:
        sql_conn = conectar_bdStores_Navicat_SQL()
        sql_cursor = sql_conn.cursor()
        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        sql_cursor.execute(f"""
                            select 
                            nombre_contrata,	
                            cliente,
                            sot,
                            estado_agendamiento,
                            tipo_trabajo,
                            departamento,
                            convert(int,customer_id)as customer_id,
                            operador,
                            responsable,
                            validacion,
                            subestado,
                            motivo,
                            skyway,
                            afectacion,
                            desalineacion,
                            servicio_afectado,
                            inconveniente,
                            observacion,
                            fecha_inicio,
                            fecha_fin,
                            tmo
                            from tblValidacionRemotaBD
                            where validacion <> 'GESTIONADA' and convert(date,fecha_inicio) between '{fecha_inicio}' and '{fecha_fin}'
                        """
                             )
        datos_sql_server = sql_cursor.fetchall()

        
        mysql_conn=conectar_bdStores_Navicat2()
        
        try:
            mysql_cursor = mysql_conn.cursor()
            # Código que usa mysql_cursor
        except Exception as e:
            print(f"Error al inicializar el cursor: {e}")
        


        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        insert_query = """
            INSERT INTO VALIDACION_REMOTA_AMG (`NOMBRE_CONTRATA`,	`CLIENTE`,	`SOT`,	`ESTADO_AGENDAMIENTO`,	`TIPO_DE_TRABAJO`,	`DEPARTAMENTO`,	`CUSTOMER_ID`,	`OPERADOR`,	`RESPONSABLE`,	`VALIDACION`,	`SUBESTADO`,	`MOTIVO`,	`SKYWAY`,	`AFECTACION`,	`DESALINEACION`,	`SERVICIO_AFECTADO`,	`INCONVENIENTE`,	`OBSERVACION`,	`FECHA_INICIO`,	`FECHA_FIN`,	`TMO`)
            VALUES (%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s)"""
        # Reemplazar None por NULL en las tuplas antes de la inserción
        data_to_insert = [tuple(None if val is None else val for val in row) for row in datos_sql_server]
        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        mysql_cursor.executemany(insert_query, data_to_insert)
        # Commit para aplicar los cambios
        mysql_conn.commit()
    ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")
    except Exception as e:
        print(f"Error desconocido: {e}")
    finally:
    # Cerrar las conexiones y los cursores
        if sql_cursor:
            sql_cursor.close()
        if sql_conn:
            sql_conn.close()
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()

        print("Datos transferidos correctamente")

def Encuesta_Detalle_navicat(fecha_inicio, fecha_fin):
    try:
        sql_conn = conectar_bdStores_Navicat_SQL()
        sql_cursor = sql_conn.cursor()
        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        sql_cursor.execute(f"""
                        select 
                        convert(int,id) as ID,
                        convert (int,[n_de_sot]) as SOT,
                        nombre_del_cliente as NOMBRE_CLIENTE,
                        departamento as DEPARTAMENTO,
                        null as 'PROVINCIA',
                        null as 'DISTRITO',
                        nombre_del_tecnico as NOMBRE_TECNICO,
                        convert(int,dni_tecn) as DNI_TECN,
                        convert(float,rpc) as	RPC,
                        contrata as CONTRATA,
                        rechazo_administrativo as RECHAZO_ADMINISTRATIVO,
                        comentario_rechazo as COMENTARIO_RECHAZO,
                        motivo_rechazo as MOTIVO_RECHAZO,
                        usuario_rechazo as USUARIO_RECHAZO,
                        tipo_usuario as	TIPO_USUARIO,
                        convert(int,codigo_agente) as CODIGO_AGENTE,
                        observacion_tecn as OBSERVACION_TECN,
                        imei as	IMEI,
                        latitud as LATITUD,
                        longitud as LONGITUD,
                        latitud_header as LATITUD_HEADER,
                        longitud_header as LONGITUD_HEADER,
                        distancia as DISTANCIA,
                        producto as PRODUCTO,
                        tipo_servicio as TIPO_SERVICIO,
                        servicio_contratado as SERVICIO_CONTRATADO,
                        cantidad_deco as CANTIDAD_DECO,
                        escenario as ESCENARIO,
                        descripcion_escenario as DESCRIPCION_ESCENARIO,
                        tipo_decodificador as	TIPO_DECODIFICADOR,
                        velocidad_contratada as	VELOCIDAD_CONTRATA,
                        convert(int,celular_tecnico_actual) as CELULAR_TECNICO_ACTUAL,
                        operatividad_servicio as OPERATIVIDAD_SERVICIO,
                        persona_atendio as PERSONA_ATENDIO,
                        convert(int,documento_atendio) as DOCUMENTO_ATENDIO,
                        nombre_atendio as NOMBRE_ATENDIO,
                        parentesco as PARENTESCO,
                        resultado as RESULTADO,
                        subresultado as SUBRESULTADO,
                        observacion as OBSERVACION,
                        status as STATUS,
                        falla_amg as FALLA_AMG,
                        null as HORA_INICIO_FOTO,
                        null as HORA_FIN_FOTO,
                        hora_inicio_contrata as	HORA_INICIO_CONTRATA,
                        hora_inicio_call_center as HORA_INICIO_CALLCENTER,
                        hora_fin_call_center as HORA_FIN_CALLCENTER
                        FROM TblEncuestaDetalleBD
                        where convert (date, hora_inicio_contrata) between '{fecha_inicio}' and '{fecha_fin}'
                        """
                             )
        datos_sql_server = sql_cursor.fetchall()

        
        mysql_conn=conectar_bdStores_Navicat2()
        
        try:
            mysql_cursor = mysql_conn.cursor()
            # Código que usa mysql_cursor
        except Exception as e:
            print(f"Error al inicializar el cursor: {e}")
        


        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        insert_query = """
            INSERT INTO REPORTE_VIDEOLLAMADA (`ID`,	`SOT`,	`NOMBRE_CLIENTE`,	`DEPARTAMENTO`,	`PROVINCIA`,	`DISTRITO`,	`NOMBRE_TECNICO`,	`DNI_TECN`,	`RPC`,	`CONTRATA`,	`RECHAZO_ADMINISTRATIVO`,	`COMENTARIO_RECHAZO`,	`MOTIVO_RECHAZO`,	`USUARIO_RECHAZO`,	`TIPO_USUARIO`,	`CODIGO_AGENTE`,	`OBSERVACION_TECN`,	`IMEI`,	`LATITUD`,	`LONGITUD`,	`LATITUD_HEADER`,	`LONGITUD_HEADER`,	`DISTANCIA`,	`PRODUCTO`,	`TIPO_SERVICIO`,	`SERVICIO_CONTRATADO`,	`CANTIDAD_DECO`,	`ESCENARIO`,	`DESCRIPCION_ESCENARIO`,	`TIPO_DECODIFICADOR`,	`VELOCIDAD_CONTRATA`,	`CELULAR_TECNICO_ACTUAL`,	`OPERATIVIDAD_SERVICIO`,	`PERSONA_ATENDIO`,	`DOCUMENTO_ATENDIO`,	`NOMBRE_ATENDIO`,	`PARENTESCO`,	`RESULTADO`,	`SUBRESULTADO`,	`OBSERVACION`,	`STATUS`,	`FALLA_AMG`,	`HORA_INICIO_FOTO`,	`HORA_FIN_FOTO`,	`HORA_INICIO_CONTRATA`,	`HORA_INICIO_CALLCENTER`,	`HORA_FIN_CALLCENTER`)
            VALUES (%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s)"""
        # Reemplazar None por NULL en las tuplas antes de la inserción
        data_to_insert = [tuple(None if val is None else val for val in row) for row in datos_sql_server]
        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        mysql_cursor.executemany(insert_query, data_to_insert)
        # Commit para aplicar los cambios
        mysql_conn.commit()
    ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")
    except Exception as e:
        print(f"Error desconocido: {e}")
    finally:
    # Cerrar las conexiones y los cursores
        if sql_cursor:
            sql_cursor.close()
        if sql_conn:
            sql_conn.close()
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()

        #print("Datos transferidos correctamente")

