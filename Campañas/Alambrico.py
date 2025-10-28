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
    
def CargaNominaAlambrico(fecha_fin):
    
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
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\Fotos_Alambrico\{año}\{mesNombre}\nomina_{hoy.strftime('%Y%m')}.xlsx"
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
            print("No se encontraron hojas válidas.")
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

            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\Fotos_Alambrico\{año}\{mesNombre}\Consolidado {mesNombre}.xlsx"

            if os.path.exists(excel_file_path):
                os.remove(excel_file_path)

            df_final.to_excel(excel_file_path, index=False)
            print(f"Datos guardados en el archivo {excel_file_path}.")

        except Exception as e:
            logging.warning(f"\n❌ Error al subir a la base de datos: {e}")
    #return ultimo_log_hoja  # ← Aquí devolvemos el último log
    # conexion = conectar_bdStores()
    # try:
        
    #     cursor = conexion.cursor()
    #     parametros = (año,mes)  # Tupla de tres valores

    #     # Llamar al procedimiento almacenado
    #     cursor.callproc('Sp_ActualizacionNomina_alambrico', parametros)

    #     # Obtener el resultado
    #     result = cursor.fetchone()
    #     conexion.commit() 
    #     print(f"Resultado obtenido: {result}")  # Depuración, muestra el resultado antes de procesar

    #     if result:  # Si hay resultados
    #         return result['Total']  # Accede a la clave 'Total' del diccionario
    #     else:
    #         return "No Data"  # Si no hay resultados

    # except pymssql.DatabaseError as e:
    #     # Manejo de errores específicos de la base de datos
    #     logging.warning(f"Error en la base de datos: {e}")
    #     return f"Error en la base de datos: {e}"

    # except Exception as e:
    #     # Captura de la traza completa del error
    #     import traceback
    #     error_details = traceback.format_exc()
    #     logging.warning(f"Error ocurrió: {error_details}")  # Imprime el error completo
    #     return f"Error en la obtención de datos: {error_details}"

    # finally:
    #     # Asegurarse de cerrar tanto el cursor como la conexión
    #     if cursor:
    #         cursor.close()
    #     if conexion:
    #         conexion.close()                
    #     if 'excel' in locals():
    #             excel.close()

def Campaña_Alambrico(fecha_inicio, fecha_fin):
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
    tables = ["TblFotosAlambricoExcel"]

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
        ruta_Alambrico = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Fotos Alambrico\{mesNombre}\alambrico{dia:02d}.csv"


        if os.path.exists(ruta_Alambrico):
            try:
                dtype_especifico = {
                    'DNI_TECN': str
                }

                df_merged_Alambrico = pd.read_csv(ruta_Alambrico, sep=',', encoding='utf-8',dtype=dtype_especifico)
                df_merged_Alambrico.iloc[:, 32].unique()
                df_merged_Alambrico.columns = [normalize_column_name(col) for col in df_merged_Alambrico.columns]
                df_merged_Alambrico['hora_inicio_contrata'] = pd.to_datetime(df_merged_Alambrico['hora_inicio_contrata'])
                df_merged_Alambrico['hora_inicio_call_center'] = pd.to_datetime(df_merged_Alambrico['hora_inicio_call_center'])
                df_merged_Alambrico['hora_fin_call_center'] = pd.to_datetime(df_merged_Alambrico['hora_fin_call_center'])
                df_merged_Alambrico['fecha_foto'] = pd.to_datetime(df_merged_Alambrico['fecha_foto'], format='mixed', errors='coerce')

                with engine.connect() as connection:
                    df_merged_Alambrico.to_sql('TblFotosAlambricoExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Alambrico cargado exitosamente para el día {dia}: {ruta_Alambrico}")
            except Exception as e:
                logging.error(f"Error procesando archivo Alambrico {ruta_Alambrico} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Alambrico no encontrado para el día {dia}: {ruta_Alambrico}")

    ##############################################################################################
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_CampañaFotosAlambrico_rango', parametros)
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

def KpiAlambrico(fecha_fin):
    
    
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
        cursor.callproc('SP_KpiAlambrico', parametros)
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

def Campaña_Alambrico_Rd_Amg_App(fecha_inicio, fecha_fin):
    sql_conn = None
    sql_cursor = None
    mysql_conn = None
    mysql_cursor = None

    try:
        sql_conn = conectar_bdStores_Navicat_SQL()
        sql_cursor = sql_conn.cursor()
        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        sql_cursor.execute(f"""
                            SELECT id_salesys,convert(int,[n_de_sot])as n_de_sot,	[nombre_del_cliente],	[departamento],	[nombre_del_tecnico],	
                            convert(int,[dni_tecn]) as [dni_tecn],	
                            [contrata],	[rechazo_administrativo],	[comentario_rechazo],	[motivo_rechazo],	[usuario_que_rechazo],	[tipo_usuario],
                            convert(int,[codigo_agente]) as [codigo_agente],	[observacion_tecn],	[imei],	[latitud],	[longitud],	[latitud_header],	[longitud_header],	[distancia],	[tipo_red],	[tipo_trabajo],	[tipo_servicio],	[cantidad_deco],	[numero_tarjeta],	[descripcion_actividad],	[escenario],	[descripcion_escenario],	[modelo_deco],	[modelo_emta],	[modelo_ont],	[cable_analogico],	[demora_carga_emta],	[demora_carga_ont],	[derivado_sistema],	[derivado_planta_externa],	[regularizacion],	[marca_tv],
                            convert(varchar,[cintillo]),	
                            [nombre_red_wifi],	[dispositivos],	[dispositivos_claro],	[conector],	[tipo_cableado],	[tipo_decodificador],	[codigo_solucion],	[velocidad_contratada],	[resultado],	[subresultado],	[observacion],	[status],	[falla_amg],	[fecha_foto],	[fecha_foto_dp01f_h],	[hora_inicio_contrata],	[hora_inicio_call_center],	[hora_fin_call_center],	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,	null,status_caso
                            FROM TblFotosAlambricoBD  WHERE fechafiltro between '{fecha_inicio}' and '{fecha_fin}' AND resultado<>'Pendiente'
                        """
                             )
        datos_sql_server = sql_cursor.fetchall()

        mysql_conn = conectar_bdStores_Navicat2()
        mysql_cursor = mysql_conn.cursor()


        ############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        insert_query = """
        INSERT INTO RD_AMG_APP (`id`,`N. de SOT`,	`Nombre del cliente`,	`Departamento`,	`Nombre del tecnico`,	`DNI_TECN`,	`Contrata`,	`Rechazo administrativo`,	`Comentario rechazo`,	`Motivo rechazo`,	`Usuario que rechazo`,	`Tipo usuario`,	`Codigo agente`,	`Observacion tecn`,	`IMEI`,	`Latitud`,	`Longitud`,	`Latitud Header`,	`Longitud Header`,	`Distancia`,	`Tipo red`,	`Tipo trabajo`,	`Tipo servicio`,	`Cantidad deco`,	`Numero tarjeta`,	`Descripcion actividad`,	`Escenario`,	`Descripcion escenario`,	`Modelo_deco`,	`Modelo_emta`,	`Modelo_ont`,	`Cable_analogico`,	`Demora_carga_emta`,	`Demora_carga_ont`,	`Derivado_sistema`,	`Derivado_planta_externa`,	`Regularizacion`,	`Marca_tv`,	`Cintillo`,	`Nombre_red_wifi`,	`Dispositivos`,	`Dispositivos_claro`,	`Conector`,	`Tipo_cableado`,	`Tipo_decodificador`,	`Codigo solucion`,	`Velocidad contratada`,	`Resultado`,	`Subresultado`,	`Observacion`,	`Status`,	`Falla AMG`,	`Fecha foto`,	`Fecha foto DP01F/H`,	`Hora inicio contrata`,	`Hora inicio call center`,	`Hora fin call center`,	`Descargo_Contrata`,	`Observacion_Contrata`,	`Fec_Descargo`,	`Respuesta_Claro`,	`Revision_Foto`,	`Observacion_Claro`,	`Supervisor_Claro`,	`Fec_Revision`,	`Usuario_Rev_Foto`,	`Estado_AMG`,	`Motivo_AMG`,	`Observacion_AMG`,	`Auditor_AMG`,	`Fec_AMG`,	`Confirmar_AMG`,	`Instancia_Final`,	`Estado_AMG_Final`,	`Penalizado`,	`Observacion_penalizacion`,`status_caso`)
        VALUES (%s,%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,%s)"""

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
        if sql_cursor:
            sql_cursor.close()
        if sql_conn:
            sql_conn.close()
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()

        print("Datos transferidos correctamente")