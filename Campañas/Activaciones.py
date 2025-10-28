import pandas as pd
from Campañas.funcion import *
from conexion import *
from Campañas.ocupacion_activaciones import *
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

def CargaNominaActivaciones(fecha_fin):
    
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
    archivo_excel = fr"\\SRV-FS\Repositorio_Camp_AMG\Activaciones\{año}\{mesNombre}\nomina_{hoy.strftime('%Y%m')}.xlsx"
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
                    # if 'fecha' in df.columns:
                    #     df = df.drop(columns=['fecha'])
                    # df['fecha'] = fecha_hoja
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

            excel_file_path = fr"\\SRV-FS\Repositorio_Camp_AMG\Activaciones\{año}\{mesNombre}\Consolidado {mesNombre}.xlsx"

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
        cursor.callproc('Sp_ActualizacionNomina_Activaciones', parametros)

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

def Campaña_Activaciones(fecha_inicio, fecha_fin):
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
    tables = ["TblActivacionesHFCExcel",
              "TblActivacionesEmpresaExcel",
              "TblActivacionesLTEExcel",
              "TblActivacionesFTTHExcel",
              "TblActivacionesOTROSExcel"]

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
        ruta_Activaciones_HFC = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones\{mesNombre}\HFC\hfc{dia:02d}.csv"


        if os.path.exists(ruta_Activaciones_HFC):
            try:



                df_merged_HFC = pd.read_csv(ruta_Activaciones_HFC,sep=',',encoding='latin1') #separador de , en el CSV#

                df_merged_HFC.columns = [normalize_column_name(col) for col in df_merged_HFC.columns]
                df_merged_HFC['hora_inicio_contrata'] = df_merged_HFC['hora_inicio_contrata'].apply(parse_fecha) 
                df_merged_HFC['hora_inicio_call_center'] = df_merged_HFC['hora_inicio_call_center'].apply(parse_fecha) 
                df_merged_HFC['hora_fin_call_center'] = df_merged_HFC['hora_fin_call_center'].apply(parse_fecha) 
                
                df_merged_HFC['nombre_usuario'] = df_merged_HFC['nombre_usuario'].astype(str).str.replace('A', '0')

                with engine.connect() as connection:
                    df_merged_HFC.to_sql('TblActivacionesHFCExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo HFC cargado exitosamente para el día {dia}: {ruta_Activaciones_HFC}")
            except Exception as e:
                logging.error(f"Error procesando archivo HFC {ruta_Activaciones_HFC} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo HFC no encontrado para el día {dia}: {ruta_Activaciones_HFC}")
    ##############################################################################################
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_Activaciones_EMPRESA = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones\{mesNombre}\EMPRESA\empresa{dia:02d}.csv"

        if os.path.exists(ruta_Activaciones_EMPRESA):
            try:


                df_merged_EMPRESA = pd.read_csv(ruta_Activaciones_EMPRESA,sep=',',encoding='latin1') #separador de , en el CSV#


                df_merged_EMPRESA.columns = [normalize_column_name(col) for col in df_merged_EMPRESA.columns]
                df_merged_EMPRESA['hora_inicio_contrata'] = df_merged_EMPRESA['hora_inicio_contrata'].apply(parse_fecha) 
                df_merged_EMPRESA['hora_inicio_call_center'] = df_merged_EMPRESA['hora_inicio_call_center'].apply(parse_fecha) 
                df_merged_EMPRESA['hora_fin_call_center'] = df_merged_EMPRESA['hora_fin_call_center'].apply(parse_fecha) 
                            
                df_merged_EMPRESA['nombre_usuario'] = df_merged_EMPRESA['nombre_usuario'].astype(str).str.replace('A', '0')

                with engine.connect() as connection:
                    df_merged_EMPRESA.to_sql('TblActivacionesEmpresaExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo EMPRESA cargado exitosamente para el día {dia}: {ruta_Activaciones_EMPRESA}")
            except Exception as e:
                logging.error(f"Error procesando archivo EMPRESA {ruta_Activaciones_EMPRESA} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo EMPRESA no encontrado para el día {dia}: {ruta_Activaciones_EMPRESA}")
    ##############################################################################################
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_Activaciones_LTE = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones\{mesNombre}\LTE\lte{dia:02d}.csv"

        if os.path.exists(ruta_Activaciones_LTE):
            try:


                df_merged_LTE = pd.read_csv(ruta_Activaciones_LTE,sep=',',encoding='latin1') #separador de , en el CSV#


                df_merged_LTE.columns = [normalize_column_name(col) for col in df_merged_LTE.columns]
                df_merged_LTE['hora_inicio_contrata'] = df_merged_LTE['hora_inicio_contrata'].apply(parse_fecha) 
                df_merged_LTE['hora_inicio_call_center'] = df_merged_LTE['hora_inicio_call_center'].apply(parse_fecha) 
                df_merged_LTE['hora_fin_call_center'] = df_merged_LTE['hora_fin_call_center'].apply(parse_fecha)
                            
                df_merged_LTE['nombre_usuario'] = df_merged_LTE['nombre_usuario'].astype(str).str.replace('A', '0')

                with engine.connect() as connection:
                    df_merged_LTE.to_sql('TblActivacionesLTEExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo EMPRESA cargado exitosamente para el día {dia}: {ruta_Activaciones_LTE}")
            except Exception as e:
                logging.error(f"Error procesando archivo EMPRESA {ruta_Activaciones_LTE} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo EMPRESA no encontrado para el día {dia}: {ruta_Activaciones_LTE}")
    ##############################################################################################
    
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_Activaciones_FTTH = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones\{mesNombre}\FTTH\ftth{dia:02d}.csv"


        if os.path.exists(ruta_Activaciones_FTTH):
            try:


                df_merged_FTTH = pd.read_csv(ruta_Activaciones_FTTH,sep=',',encoding='latin1') #separador de , en el CSV#


                df_merged_FTTH.columns = [normalize_column_name(col) for col in df_merged_FTTH.columns]
                df_merged_FTTH['hora_inicio_contrata'] = df_merged_FTTH['hora_inicio_contrata'].apply(parse_fecha) 
                df_merged_FTTH['hora_inicio_call_center'] = df_merged_FTTH['hora_inicio_call_center'].apply(parse_fecha) 
                df_merged_FTTH['hora_fin_call_center'] = df_merged_FTTH['hora_fin_call_center'].apply(parse_fecha)
                            
                df_merged_FTTH['nombre_usuario'] = df_merged_FTTH['nombre_usuario'].astype(str).str.replace('A', '0')

                with engine.connect() as connection:
                    df_merged_FTTH.to_sql('TblActivacionesFTTHExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo FTTH cargado exitosamente para el día {dia}: {ruta_Activaciones_FTTH}")
            except Exception as e:
                logging.error(f"Error procesando archivo FTTH {ruta_Activaciones_FTTH} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo FTTH no encontrado para el día {dia}: {ruta_Activaciones_FTTH}")
    ##############################################################################################
 
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_Activaciones_OTROS = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones\{mesNombre}\OTROS\otros{dia:02d}.csv"

        if os.path.exists(ruta_Activaciones_OTROS):
            try:

                df_merged_OTROS = pd.read_csv(ruta_Activaciones_OTROS,sep=',',encoding='latin1') #separador de , en el CSV#  


                df_merged_OTROS.columns = [normalize_column_name(col) for col in df_merged_OTROS.columns]
                df_merged_OTROS['hora_inicio_contrata'] = df_merged_OTROS['hora_inicio_contrata'].apply(parse_fecha) 
                df_merged_OTROS['hora_inicio_call_center'] = df_merged_OTROS['hora_inicio_call_center'].apply(parse_fecha) 
                df_merged_OTROS['hora_fin_call_center'] = df_merged_OTROS['hora_fin_call_center'].apply(parse_fecha)
                            
                df_merged_OTROS['nombre_usuario'] = df_merged_OTROS['nombre_usuario'].astype(str).str.replace('A', '0')

                with engine.connect() as connection:
                    df_merged_OTROS.to_sql('TblActivacionesOTROSExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo FTOTROSTH cargado exitosamente para el día {dia}: {ruta_Activaciones_OTROS}")
            except Exception as e:
                logging.error(f"Error procesando archivo OTROS {ruta_Activaciones_OTROS} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo OTROS no encontrado para el día {dia}: {ruta_Activaciones_OTROS}")
    ##############################################################################################   

    log_subprocess(f"🚀 Iniciando procesamiento de ocupación desde {fecha_ini} hasta {fecha_f}")

    engine = conectar_bdCargaExcel()

    current_date = fecha_ini
    fechas_procesadas = 0

    while current_date <= fecha_f:
        fecha_str = current_date.strftime('%Y-%m-%d')
        log_subprocess(f"📅 Procesando fecha: {fecha_str}")

        try:
            with engine.connect() as connection:
                # Activaciones
                df = pd.read_sql(f"""
                    SELECT nombre_usuario codigo_salesys, asesor, hora_inicio_call_center, hora_fin_call_center
                    FROM TblActivacionesBD
                    WHERE CONVERT(DATE, hora_inicio_call_center ) = '{fecha_str}'
                """, con=connection)
                # Franjas
                df_Franjas = pd.read_sql(f"""
                                select * from TblFranjasActivaciones
                """, con=connection)
                # Estado agente
                df_2 = pd.read_sql(f"""
                    SELECT CONVERT(DATE, hora_inicio) fecha, codigo_del_agente codigo_salesys,
                            [FUNCION] funcion, [hora_inicio], [hora_fin]
                    FROM TblEstadoAgenteSaleSysBD
                    WHERE CONVERT(DATE,[hora_inicio]) = '{fecha_str}'
                """, con=connection)

                # Nómina
                df_3 = pd.read_sql(f"""
                    SELECT [fecha], [Codigo SaleSys] codigo_salesys, [Nombre Completo] nombre,
                            [condicion], [cargo], [CAMPAÑA] campana
                    FROM View_TblNomina
                    WHERE CONVERT(DATE, [fecha]) = '{fecha_str}' AND campaña = 'ACTIVACIONES'
                """, con=connection)

            df_activaciones = df.copy()
            df_estado_agente = df_2.copy()
            franjas = df_Franjas.copy()
            df_nomina = df_3.copy()

            # Procesamiento de franjas
            franjas['Fecha_Hora_Inicio'] = pd.to_datetime(franjas['Fecha_Hora_Inicio'], format='%d-%m-%Y %H:%M:%S')
            franjas['Fecha_Hora_Fin'] = pd.to_datetime(franjas['Fecha_Hora_Fin'], format='%d-%m-%Y %H:%M:%S')
            franjas.columns = [normalize_column_name(col) for col in franjas.columns]

            # Conversión de tipos
            df_2['fecha'] = pd.to_datetime(df_2['fecha'])
            df_3['codigo_salesys'] = df_3['codigo_salesys'].astype('Int64')
            df_3['fecha'] = pd.to_datetime(df_3['fecha'])


            # Filtrar estado agente
            df_estado_agente_sig_on = df_estado_agente[df_estado_agente['funcion'] == 'SON - Sign On'].copy()
            df_estado_agente_res_resume = df_estado_agente[df_estado_agente['funcion'] == 'RES - RESUME'].copy()

            # Calcular tiempos totales
            df_estado_agente_res_resume['total_sec'] = (df_estado_agente_res_resume['hora_fin'] - df_estado_agente_res_resume['hora_inicio']).dt.total_seconds().astype('Int64')
            df_estado_agente_sig_on['total_sec'] = (df_estado_agente_sig_on['hora_fin'] - df_estado_agente_sig_on['hora_inicio']).dt.total_seconds().astype('Int64')

            # Filtrar registros >= 30 segundos
            filtro_res_resume = df_estado_agente_res_resume[df_estado_agente_res_resume['total_sec'] >= 30]
            filtro_sig_on = df_estado_agente_sig_on[df_estado_agente_sig_on['total_sec'] >= 30]

            df_estado_agente_res_resume_filtro = filtro_res_resume.drop('total_sec', axis=1)
            df_estado_agente_sig_on_filtro = filtro_sig_on.drop('total_sec', axis=1)

            # Merge con nómina
            filtro_res_resume_por_nomina = df_estado_agente_res_resume_filtro.merge(df_nomina, on=['codigo_salesys', 'fecha'])
            filtro_sig_on_por_nomina = df_estado_agente_sig_on_filtro.merge(df_nomina, on=['codigo_salesys', 'fecha'])

            # Generar tiempos por franjas
            df_resultado_sig_on = generar_tiempos_por_franja(filtro_sig_on_por_nomina, franjas)
            df_resultado_res_resume = generar_tiempos_por_franja(filtro_res_resume_por_nomina, franjas)

            # Consolidar datos
            df_consolidado = pd.concat([df_resultado_sig_on, df_resultado_res_resume])
            df_consolidado['fecha'] = pd.to_datetime(df_consolidado['fecha'])

            # Procesar activaciones
            df_activaciones['codigo_salesys'] = df_activaciones['codigo_salesys'].astype('Int64')

            # Agrupar tiempos por franja
            df_consolidado_agrupado = df_consolidado.groupby(['codigo_salesys', 'funcion', 'fecha', 'franja']).agg({'tiempo_segundos': 'sum'}).reset_index()
            df_consolidado_agrupado['funcion'] = 'DISPONIBLE'

            # Agrupar por agente, fecha, franja
            df_consolidado_final = df_consolidado_agrupado.groupby(['fecha', 'codigo_salesys', 'franja']).agg({'tiempo_segundos': 'sum'}).reset_index()
            df_consolidado_final['tiempo_segundos'] = df_consolidado_final['tiempo_segundos'].astype('Int64')
            
            df_consolidado_final['fecha'] = pd.to_datetime(df_consolidado_final['fecha'])
            df_nomina['fecha'] = pd.to_datetime(df_nomina['fecha'])
            # Merge con nómina
            es_agente_nomina = pd.merge(
                df_consolidado_final,
                df_nomina[['fecha', 'codigo_salesys', 'nombre', 'condicion', 'cargo', 'campana']],
                on=['fecha', 'codigo_salesys'],
                how='left'
            )

            # Ordenar columnas
            columnas_agen_nom = ['fecha', 'codigo_salesys', 'nombre', 'condicion', 'cargo', 'campana', 'franja', 'tiempo_segundos']
            es_agente_nomina_select = es_agente_nomina[columnas_agen_nom]
            es_agente_nomina_select['codigo_salesys'] = es_agente_nomina_select['codigo_salesys'].astype('Int64')

            # Procesar gestiones
            columnas_validaciones = ['asesor', 'codigo_salesys', 'hora_inicio_call_center', 'hora_fin_call_center']
            df_activaciones_select2 = df_activaciones[columnas_validaciones]

            # Mapear segundos por franja
            df_resultado = mapear_segundos_por_franja(df_activaciones_select2, franjas)
            df_resultado['fecha'] = pd.to_datetime(df_resultado['fecha'])
            df_resultado['tiempo_segundos'] = df_resultado['tiempo_segundos'].astype('int64')

            # Agrupar gestiones por franja
            df_agrupado = df_resultado.groupby(['fecha', 'codigo_salesys', 'franja']).agg({'tiempo_segundos': 'sum'}).reset_index()
            df_agrupado_2 = df_agrupado.rename(columns={'tiempo_segundos': 'segundos_gestionados'})
            df_agrupado_2['codigo_salesys'] = df_agrupado_2['codigo_salesys'].astype('Int64')

            # Merge final
            df_agrupado_final = pd.merge(
                df_agrupado_2,
                df_nomina[['fecha', 'codigo_salesys', 'nombre']],
                on=['fecha', 'codigo_salesys'],
                how='left'
            )

            # Renombrar columnas
            es_agente_nomina_select = es_agente_nomina_select.rename(columns={'tiempo_segundos': 'segundos_disponible'})

            # Merge ocupación final
            ocupacion_final = pd.merge(
                es_agente_nomina_select,
                df_agrupado_final[['fecha', 'codigo_salesys', 'franja', 'segundos_gestionados']],
                on=['fecha', 'codigo_salesys', 'franja'],
                how='left'
            )

            # Procesar franjas para merge final
            franjas['fecha_hora_inicio'] = pd.to_datetime(franjas['fecha_hora_inicio'], format='%d-%m-%Y %H:%M:%S')
            franjas['fecha'] = franjas['fecha_hora_inicio'].dt.date
            franjas['hora_inicio'] = franjas['fecha_hora_inicio'].dt.time
            franjas['fecha'] = pd.to_datetime(franjas['fecha'])
            franjas = franjas.rename(columns={'etiqueta_franja': 'franja'})

            # Merge con franjas
            df_agrupado_final_franjas = pd.merge(
                ocupacion_final,
                franjas[['fecha', 'franja', 'hora_inicio']],
                on=['fecha','franja'],
                how='left'
            )

            df_to_sql = df_agrupado_final_franjas.rename(columns={'hora_inicio': 'rango_15min'})

            # Eliminar registros existentes
            with engine.connect() as connection:
                delete_query = text(f"DELETE FROM Tbl_Ocupacion_Activaciones WHERE fecha = '{fecha_str}'")
                connection.execute(delete_query)
                connection.execute(text("COMMIT"))

            # Cargar datos a la base
            with engine.connect() as connection:
                df_to_sql.to_sql('Tbl_Ocupacion_Activaciones', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            log_subprocess(f"✅ Fecha {fecha_str} procesada exitosamente - {len(df_to_sql)} registros cargados")
            fechas_procesadas += 1


        except Exception as e:
            log_subprocess(f"❌ Error al procesar fecha {fecha_str}: {str(e)}")

        finally:
            current_date += timedelta(days=1)  # Avanzar siempre
##################################################################################################################
    # log_subprocess(f"🚀 Iniciando procesamiento de averías desde {fecha_inicio} hasta {fecha_fin}")
    
    # engine = conectar_bdCargaExcel()
    # archivo_averias = fr'\\SRV-FS\CompartidoActivaciones\Supervision\INCIDENCIAS Y AVERIAS 2025.xlsx'

    # try:
    #     df = pd.read_excel(archivo_averias, sheet_name='CLARO', dtype={'PLUME': str})
    #     log_subprocess("✅ Archivo de averías cargado exitosamente")
    # except Exception as e:
    #     log_subprocess(f"❌ Error cargando archivo de averías: {e}")
    #     return False

    # try:
    #     try:
    #         df = pd.read_excel(archivo_averias, sheet_name='CLARO', dtype={'PLUME': str})
    #         log_subprocess("✅ Archivo de averías cargado exitosamente")
    #     except Exception as e:
    #         log_subprocess(f"❌ Error cargando archivo de averías: {e}")
    #         return False
        
    #     df_filt = df[(df['f inicio'] >= fecha_ini)]
    #     df_filt = df_filt[(df_filt['f inicio'] <= fecha_f)]
    #     df_filtro = df_filt[(df_filt['FECHA FIN'].notna())]

    #     # if df_filtro.empty:
    #     #     log_subprocess(f"⚠️ No hay datos de averías para el rango {fecha_inicio} - {fecha_fin}")
    #     #     return True
    #     df_filtro['Fin'] = pd.to_datetime(df_filtro['Fin'])


    #     # Filtro de fechas y datos válidos
    #     df['f inicio'] = pd.to_datetime(df['f inicio'], errors='coerce')
    #     df_filt = df[(df['f inicio'] >= fecha_ini) & (df['f inicio'] <= fecha_f)]
    #     df_filtro = df_filt[df_filt['FECHA FIN'].notna()].copy()
        
    #     log_subprocess(f"📊 Procesando {len(df_filtro)} registros de averías")

    #     # Eliminar columnas innecesarias y calcular duración
    #     df_drop = df_filtro.drop(columns=['f inicio', 'H. INICIO', 'FECHA FIN','H. FIN'], errors='ignore').copy()
    #     df_drop['DURACION'] = df_drop['Fin'] - df_drop['Inicio']

    #     # Aplicar función de conversión a formato hh:mm:ss
    #     df_drop['DURACION'] = df_drop['DURACION'].apply(timedelta_to_hms)
        
    #     # Filtrar solo registros que impactan en NS
    #     df_filtro = df_drop[(df_drop['IMPACTA EN EL NS'] == 'SI')]
        
    #     # if df_filtro.empty:
    #     #     log_subprocess(f"⚠️ No hay registros que impacten en NS para el rango especificado")
    #     #     return True

    #     log_subprocess(f"📊 {len(df_filtro)} registros impactan en NS")


    #     # Procesamiento de columnas
    #     # Procesar datos
    #     df_filtro_copy = df_filtro.copy()
        
    #     # Reemplazar valores en columnas específicas
    #     df_filtro_copy['ACTIVACION'] = df_filtro_copy['ACTIVACION'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
    #     df_filtro_copy['CAMBIO DE EQUIPO'] = df_filtro_copy['CAMBIO DE EQUIPO'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
    #     df_filtro_copy['POSTVENTA'] = df_filtro_copy['POSTVENTA'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
    #     df_filtro_copy['REENVIO DE SENAL'] = df_filtro_copy['REENVIO DE SENAL'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
    #     df_filtro_copy['PLUME'] = df_filtro_copy['PLUME'].str.replace(' -', '-').str.replace('- ', '-')

    #     # Renombrar columnas
    #     df_filtro_copy = df_filtro_copy.rename(columns={'POSTVENTA':'POST VENTA', 'CAMBIO DE EQUIPO': 'CAMBIO EQUIPO'})

    #     # Extraer y procesar casos
    #     df_filtro_copy['caso'] = df_filtro_copy[['ACTIVACION', 'CAMBIO EQUIPO', 'POST VENTA', 'REENVIO DE SENAL', 'PLUME']].apply(
    #         lambda row: '|'.join([f"{col} {fragment}" 
    #                              for col, val in row.items() if pd.notna(val)
    #                              for fragment in str(val).split('-')]), axis=1)

    #     # Normalizar casos
    #     df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('REENVIO DE SENAL EMPRESA', 'REENVIO SENAL EMPRESA')
    #     df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('REENVIO DE SENAL FTTH', 'REENVIO SENAL FTTH')
    #     df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('PLUME PLUME WIFI ACTIVACION', 'PLUME WIFI ACTIVACION')
    #     df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('PLUME REGISTRO MESH', 'REGISTRO MESH')

    #     # Renombrar columnas finales y limpiar DataFrame
    #     df_filtro_copy = df_filtro_copy.rename(columns={'Inicio': 'fecha_hora_inicio', 'Fin': 'fecha_hora_fin', 'caso': 'skill_afectado'})
    #     df_drop_2 = df_filtro_copy.drop(columns=['ACTIVACION', 'CAMBIO DE EQUIPO', 'POST VENTA','REENVIO DE SENAL', 'PLUME', 'CAMBIO EQUIPO'], errors='ignore').copy()

    #     # Filtrar por rango de fechas en el DataFrame final
    #     df_drop_2 = df_drop_2[
    #         (df_drop_2['fecha_hora_inicio'].dt.date >= pd.to_datetime(fecha_inicio).date()) &
    #         (df_drop_2['fecha_hora_inicio'].dt.date <= pd.to_datetime(fecha_fin).date())
    #     ]

    #     if df_drop_2.empty:
    #         log_subprocess(f"⚠️ No hay registros finales para el rango {fecha_inicio} - {fecha_fin}")
    #         return True

    #     log_subprocess(f"📊 {len(df_drop_2)} registros finales a procesar")

    #     # Eliminar registros existentes en BD
    #     with engine.connect() as connection:
    #         delete_query = text(f"""
    #             DELETE FROM TblAveriasActivacionesBD 
    #             WHERE CONVERT(DATE, fecha_hora_inicio) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    #         """)
    #         connection.execute(delete_query)
    #         connection.execute(text("COMMIT"))
    #         log_subprocess(f"🗑️ Registros existentes eliminados para el rango {fecha_inicio} - {fecha_fin}")

    #     # Cargar nuevos datos
    #     with engine.connect() as connection:
    #         df_drop_2.to_sql('TblAveriasActivacionesBD', con=connection, if_exists='append', index=False)
    #         connection.execute(text("COMMIT"))

    #     log_subprocess(f"✅ Procesamiento completado: {len(df_drop_2)} registros cargados exitosamente")

    #     # Ejecutar SP
    #     try:
    #         conexion = conectar_bdStores()
    #         cursor = conexion.cursor()
    #         parametros = (fecha_inicio, fecha_fin)
    #         cursor.callproc('Sp_CampañaActivaciones_rango', parametros)
    #         conexion.commit()
    #         log_subprocess("✅ Procedimiento almacenado ejecutado correctamente")
    #     except Exception as e:
    #         import traceback
    #         error_details = traceback.format_exc()
    #         log_subprocess(f"❌ Error al ejecutar SP: {error_details}")
    #     finally:
    #         if cursor:
    #             cursor.close()
    #         if conexion:
    #             conexion.close()

    #     return True

    # except Exception as e:
    #     log_subprocess(f"❌ Error general en procesamiento: {e}")
    #     return False

    log_subprocess(f"🚀 Iniciando procesamiento de averías desde {fecha_inicio} hasta {fecha_fin}")

    engine = conectar_bdCargaExcel()
    archivo_averias = fr'\\SRV-FS\CompartidoActivaciones\Supervision\INCIDENCIAS Y AVERIAS 2025.xlsx'

    try:
        df = pd.read_excel(archivo_averias, sheet_name='CLARO', dtype={'PLUME': str})
        log_subprocess("✅ Archivo de averías cargado exitosamente")
    except Exception as e:
        log_subprocess(f"❌ Error cargando archivo de averías: {e}")
        return False

    try:
        # Filtro de fechas y datos válidos
        df['f inicio'] = pd.to_datetime(df['f inicio'], errors='coerce')
        df_filt = df[(df['f inicio'] >= fecha_ini) & (df['f inicio'] <= fecha_f)]
        df_filtro = df_filt[df_filt['FECHA FIN'].notna()].copy()
        
        # Si no hay datos de averías, continuar con DataFrame vacío (es normal)
        if df_filtro.empty:
            log_subprocess(f"ℹ️ No hay datos de averías para el rango {fecha_inicio} - {fecha_fin} (normal)")
            df_drop_2 = pd.DataFrame(columns=['fecha_hora_inicio', 'fecha_hora_fin', 'skill_afectado', 'DURACION'])
        else:
        
            log_subprocess(f"📊 Procesando {len(df_filtro)} registros de averías")

            # Eliminar columnas innecesarias y calcular duración
            df_drop = df_filtro.drop(columns=['f inicio', 'H. INICIO', 'FECHA FIN','H. FIN'], errors='ignore').copy()
            df_drop['DURACION'] = df_drop['Fin'] - df_drop['Inicio']

            # Aplicar función de conversión a formato hh:mm:ss
            df_drop['DURACION'] = df_drop['DURACION'].apply(timedelta_to_hms)
            
            # Filtrar solo registros que impactan en NS
            df_filtro_ns = df_drop[(df_drop['IMPACTA EN EL NS'] == 'SI')]
            
            # Si no hay registros que impacten en NS, continuar con DataFrame vacío (es normal)
            if df_filtro_ns.empty:
                log_subprocess(f"ℹ️ No hay registros que impacten en NS para el rango especificado (normal)")
                df_drop_2 = pd.DataFrame(columns=['fecha_hora_inicio', 'fecha_hora_fin', 'skill_afectado', 'DURACION'])
            else:
                log_subprocess(f"📊 {len(df_filtro_ns)} registros impactan en NS")

                # Procesamiento de columnas
                df_filtro_copy = df_filtro_ns.copy()
                
                # Reemplazar valores en columnas específicas
                df_filtro_copy['ACTIVACION'] = df_filtro_copy['ACTIVACION'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
                df_filtro_copy['CAMBIO DE EQUIPO'] = df_filtro_copy['CAMBIO DE EQUIPO'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
                df_filtro_copy['POSTVENTA'] = df_filtro_copy['POSTVENTA'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
                df_filtro_copy['REENVIO DE SENAL'] = df_filtro_copy['REENVIO DE SENAL'].str.replace('CE', 'EMPRESA').str.replace(' ', '')
                df_filtro_copy['PLUME'] = df_filtro_copy['PLUME'].str.replace(' -', '-').str.replace('- ', '-')

                # Renombrar columnas
                df_filtro_copy = df_filtro_copy.rename(columns={'POSTVENTA':'POST VENTA', 'CAMBIO DE EQUIPO': 'CAMBIO EQUIPO'})

                # Extraer y procesar casos
                df_filtro_copy['caso'] = df_filtro_copy[['ACTIVACION', 'CAMBIO EQUIPO', 'POST VENTA', 'REENVIO DE SENAL', 'PLUME']].apply(
                    lambda row: '|'.join([f"{col} {fragment}" 
                                        for col, val in row.items() if pd.notna(val)
                                        for fragment in str(val).split('-')]), axis=1)

                # Normalizar casos
                df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('REENVIO DE SENAL EMPRESA', 'REENVIO SENAL EMPRESA')
                df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('REENVIO DE SENAL FTTH', 'REENVIO SENAL FTTH')
                df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('PLUME PLUME WIFI ACTIVACION', 'PLUME WIFI ACTIVACION')
                df_filtro_copy['caso'] = df_filtro_copy['caso'].str.replace('PLUME REGISTRO MESH', 'REGISTRO MESH')

                # Renombrar columnas finales y limpiar DataFrame
                df_filtro_copy = df_filtro_copy.rename(columns={'Inicio': 'fecha_hora_inicio', 'Fin': 'fecha_hora_fin', 'caso': 'skill_afectado'})
                df_drop_2 = df_filtro_copy.drop(columns=['ACTIVACION', 'CAMBIO DE EQUIPO', 'POST VENTA','REENVIO DE SENAL', 'PLUME', 'CAMBIO EQUIPO'], errors='ignore').copy()

                # Filtrar por rango de fechas en el DataFrame final
                df_drop_2 = df_drop_2[
                    (df_drop_2['fecha_hora_inicio'].dt.date >= pd.to_datetime(fecha_inicio).date()) &
                    (df_drop_2['fecha_hora_inicio'].dt.date <= pd.to_datetime(fecha_fin).date())
                ]

        # Determinar el mensaje de log según si hay datos o no
        if df_drop_2.empty:
            log_subprocess(f"ℹ️ Sin registros de averías para el rango {fecha_inicio} - {fecha_fin} (enviando tabla vacía)")
        else:
            log_subprocess(f"📊 {len(df_drop_2)} registros finales a procesar")

        # Eliminar registros existentes en BD
        with engine.connect() as connection:
            delete_query = text(f"""
                DELETE FROM TblAveriasActivacionesBD 
                WHERE CONVERT(DATE, fecha_hora_inicio) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
            """)
            connection.execute(delete_query)
            connection.execute(text("COMMIT"))
            log_subprocess(f"🗑️ Registros existentes eliminados para el rango {fecha_inicio} - {fecha_fin}")

        # Cargar datos (vacíos o con registros) a la BD
        with engine.connect() as connection:
            if not df_drop_2.empty:
                df_drop_2.to_sql('TblAveriasActivacionesBD', con=connection, if_exists='append', index=False)
                log_subprocess(f"✅ {len(df_drop_2)} registros de averías cargados exitosamente")
            else:
                log_subprocess("✅ Tabla de averías limpiada (sin nuevos registros - normal)")
            connection.execute(text("COMMIT"))

        # EJECUTAR SP SIEMPRE (con o sin datos de averías)
        try:
            conexion = conectar_bdStores()
            cursor = conexion.cursor()
            parametros = (fecha_inicio, fecha_fin)
            cursor.callproc('Sp_CampañaActivaciones_rango', parametros)
            conexion.commit()
            log_subprocess("✅ Procedimiento almacenado ejecutado correctamente")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            log_subprocess(f"❌ Error al ejecutar SP: {error_details}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return True

    except Exception as e:
        log_subprocess(f"❌ Error general en procesamiento: {e}")
        return False


#aca se hizo cambio

def KpiActivaciones(fecha_fin):
    
    
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
        cursor.callproc('SP_KpiActivaciones', parametros)
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

def Campaña_Activaciones_otros(fecha_fin):
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
    tables = [
            "tblActivacionesMeshDetalleExcel",
            "tblActivacionesPlumeWIFIExcel",
            "tblActivaciónFTTHExcel",
            "tblActivaciónHFCExcel",
            "tblActivacionesReenviodeSeñalEmpresaHFCExcel",
            "tblActivacionesReenviodeSeñalFTTHExcel",
            "tblActivacionesCambioEquipoEmpresaExcel",
            "tblActivacionesCambioEquipoFTTHExcel",
            "tblActivacionesPostVentaEmpresaExcel",
            "tblActivacionesPostVentaFTTHExcel",
            "tblActivacionesPostVentaHFCExcel",
            "tblActivacionesReenviodeSenalHFCExcel",
            "tblActivacionesEmpresaExcel",
            "tblActivacionesCambioEquipoHFCExcel"

            ]

    with engine.connect() as connection:
        with connection.begin() as transaction:
            for table in tables:
                connection.execute(text(f"DELETE FROM {table}"))
                logging.info(f"Contenido eliminado de la tabla {table}")

    ################################################################################################
    # Convertir strings de fechas
    fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dia_fin = fecha_f.day
    año = fecha_f.year
    mes = fecha_f.month
    mesNombre = fecha_f.strftime("%B").capitalize()

    # Limpia el log existente antes de una nueva ejecución
    open('Campañas.log', 'w', encoding='utf-8').close()
    logging.info(f"Iniciando nueva ejecución del mes de {mesNombre}")
    ################################################################################################
    # Procesar archivos delivery por día
    #for dia in range(dia_inicio, dia_fin + 1):
    ruta_Claro_mesh_detalle					= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro mesh - detalle\{mesNombre}.csv"
    ruta_Claro_Plume_WIFI 					= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro Plume WIFI\{mesNombre}.csv"
    ruta_Claro_Activación_FTTH 				= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro Activación FTTH\{mesNombre}.csv"
    ruta_Claro_activación_HFC				= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\laro activación HFC\{mesNombre}.csv"
    ruta_Claro_reenvio_de_señal_empresa_HFC	= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro reenvio de señal empresa HFC\{mesNombre}.csv"
    ruta_Claro_reenvio_de_señal_FTTH		= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro reenvio de señal FTTH\{mesNombre}.csv"
    ruta_Claro_cambio_equipo_empresa 		= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro cambio equipo empresa\{mesNombre}.csv"
    ruta_Claro_cambio_equipo_FTTH 			= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro cambio equipo FTTH\{mesNombre}.csv"
    ruta_Claro_post_venta_empresa 			= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro post venta empresa\{mesNombre}.csv"
    ruta_Claro_post_venta_FTTH				= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro post venta FTTH\{mesNombre}.csv"
    ruta_Claro_post_venta_hfc 				= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro post venta (hfc)\{mesNombre}.csv"
    ruta_Claro_Reenvio_De_Senal_HFC 		= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro Reenvio De Señal HFC\{mesNombre}.csv"
    ruta_Claro_activacion_empresas			= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro activacion empresas\{mesNombre}.csv"
    ruta_Claro_cambio_equipo_HFC 			= fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Activaciones Detalle\Claro cambio equipo HFC\{mesNombre}.csv"

    df_merged_Claro_mesh_detalle                    = pd.read_csv(ruta_Claro_mesh_detalle,sep=',',encoding='latin1') 
    df_merged_Claro_Plume_WIFI                      = pd.read_csv(ruta_Claro_Plume_WIFI,sep=',',encoding='latin1')
    df_merged_Claro_Activación_FTTH                 = pd.read_csv(ruta_Claro_Activación_FTTH,sep=',',encoding='latin1')
    df_merged_Claro_activación_HFC                  = pd.read_csv(ruta_Claro_activación_HFC,sep=',',encoding='latin1')
    df_merged_Claro_reenvio_de_señal_empresa_HFC    = pd.read_csv(ruta_Claro_reenvio_de_señal_empresa_HFC,sep=',',encoding='latin1')
    df_merged_Claro_reenvio_de_señal_FTTH           = pd.read_csv(ruta_Claro_reenvio_de_señal_FTTH,sep=',',encoding='latin1')
    df_merged_Claro_cambio_equipo_empresa           = pd.read_csv(ruta_Claro_cambio_equipo_empresa,sep=',',encoding='latin1')
    df_merged_Claro_cambio_equipo_FTTH              = pd.read_csv(ruta_Claro_cambio_equipo_FTTH,sep=',',encoding='latin1')
    df_merged_Claro_post_venta_empresa              = pd.read_csv(ruta_Claro_post_venta_empresa,sep=',',encoding='latin1')
    df_merged_Claro_post_venta_FTTH                 = pd.read_csv(ruta_Claro_post_venta_FTTH,sep=',',encoding='latin1')
    df_merged_Claro_post_venta_hfc                  = pd.read_csv(ruta_Claro_post_venta_hfc,sep=',',encoding='latin1')
    df_merged_Claro_Reenvio_De_Senal_HFC            = pd.read_csv(ruta_Claro_Reenvio_De_Senal_HFC,sep=',',encoding='latin1')
    df_merged_Claro_activacion_empresas             = pd.read_csv(ruta_Claro_activacion_empresas,sep=',',encoding='latin1')
    df_merged_Claro_cambio_equipo_HFC               = pd.read_csv(ruta_Claro_cambio_equipo_HFC,sep=',',encoding='latin1')

    df_merged_Claro_mesh_detalle.columns = [normalize_column_name(col) for col in df_merged_Claro_mesh_detalle.columns]
    df_merged_Claro_Plume_WIFI.columns = [normalize_column_name(col) for col in df_merged_Claro_Plume_WIFI.columns]    
    df_merged_Claro_Activación_FTTH.columns = [normalize_column_name(col) for col in df_merged_Claro_Activación_FTTH.columns]
    df_merged_Claro_activación_HFC.columns = [normalize_column_name(col) for col in df_merged_Claro_activación_HFC.columns]  
    df_merged_Claro_reenvio_de_señal_empresa_HFC.columns = [normalize_column_name(col) for col in df_merged_Claro_reenvio_de_señal_empresa_HFC.columns]
    df_merged_Claro_reenvio_de_señal_FTTH.columns = [normalize_column_name(col) for col in df_merged_Claro_reenvio_de_señal_FTTH.columns]  
    df_merged_Claro_cambio_equipo_empresa.columns = [normalize_column_name(col) for col in df_merged_Claro_cambio_equipo_empresa.columns]
    df_merged_Claro_cambio_equipo_FTTH.columns = [normalize_column_name(col) for col in df_merged_Claro_cambio_equipo_FTTH.columns]  
    df_merged_Claro_post_venta_empresa.columns = [normalize_column_name(col) for col in df_merged_Claro_post_venta_empresa.columns]
    df_merged_Claro_post_venta_FTTH.columns = [normalize_column_name(col) for col in df_merged_Claro_post_venta_FTTH.columns]  
    df_merged_Claro_post_venta_hfc.columns = [normalize_column_name(col) for col in df_merged_Claro_post_venta_hfc.columns]
    df_merged_Claro_Reenvio_De_Senal_HFC.columns = [normalize_column_name(col) for col in df_merged_Claro_Reenvio_De_Senal_HFC.columns]  
    df_merged_Claro_activacion_empresas.columns = [normalize_column_name(col) for col in df_merged_Claro_activacion_empresas.columns]
    df_merged_Claro_cambio_equipo_HFC.columns = [normalize_column_name(col) for col in df_merged_Claro_cambio_equipo_HFC.columns]  

    df_merged_Claro_mesh_detalle['hora_inicio_contrata'] = df_merged_Claro_mesh_detalle['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_mesh_detalle['hora_inicio_call_center'] = df_merged_Claro_mesh_detalle['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_mesh_detalle['hora_fin_call_center'] = df_merged_Claro_mesh_detalle['hora_fin_call_center'].apply(parse_fecha)
#2. Claro_Plume_WIFI
    df_merged_Claro_Plume_WIFI['hora_inicio_contrata'] = df_merged_Claro_Plume_WIFI['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_Plume_WIFI['hora_inicio_call_center'] = df_merged_Claro_Plume_WIFI['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_Plume_WIFI['hora_fin_call_center'] = df_merged_Claro_Plume_WIFI['hora_fin_call_center'].apply(parse_fecha) 
#3. Activación_FTTH
    df_merged_Claro_Activación_FTTH['hora_inicio_contrata'] = df_merged_Claro_Activación_FTTH['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_Activación_FTTH['hora_inicio_call_center'] = df_merged_Claro_Activación_FTTH['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_Activación_FTTH['hora_fin_call_center'] = df_merged_Claro_Activación_FTTH['hora_fin_call_center'].apply(parse_fecha) 
#4. Claro_activación_HFC
    df_merged_Claro_activación_HFC['hora_inicio_contrata'] = df_merged_Claro_activación_HFC['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_activación_HFC['hora_inicio_call_center'] = df_merged_Claro_activación_HFC['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_activación_HFC['hora_fin_call_center'] = df_merged_Claro_activación_HFC['hora_fin_call_center'].apply(parse_fecha) 
#5. Claro_reenvio_de_señal_empresa_HFC
    df_merged_Claro_reenvio_de_señal_empresa_HFC['hora_inicio_contrata'] = df_merged_Claro_reenvio_de_señal_empresa_HFC['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_reenvio_de_señal_empresa_HFC['hora_inicio_call_center'] = df_merged_Claro_reenvio_de_señal_empresa_HFC['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_reenvio_de_señal_empresa_HFC['hora_fin_call_center'] = df_merged_Claro_reenvio_de_señal_empresa_HFC['hora_fin_call_center'].apply(parse_fecha) 
#6. Claro_reenvio_de_señal_FTTH
    df_merged_Claro_reenvio_de_señal_FTTH['hora_inicio_contrata'] = df_merged_Claro_reenvio_de_señal_FTTH['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_reenvio_de_señal_FTTH['hora_inicio_call_center'] = df_merged_Claro_reenvio_de_señal_FTTH['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_reenvio_de_señal_FTTH['hora_fin_call_center'] = df_merged_Claro_reenvio_de_señal_FTTH['hora_fin_call_center'].apply(parse_fecha) 
#7. Claro_cambio_equipo_empresa
    df_merged_Claro_cambio_equipo_empresa['hora_inicio_contrata'] = df_merged_Claro_cambio_equipo_empresa['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_cambio_equipo_empresa['hora_inicio_call_center'] = df_merged_Claro_cambio_equipo_empresa['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_cambio_equipo_empresa['hora_fin_call_center'] = df_merged_Claro_cambio_equipo_empresa['hora_fin_call_center'].apply(parse_fecha) 
#8. Claro_cambio_equipo_FTTH
    df_merged_Claro_cambio_equipo_FTTH['hora_inicio_contrata'] = df_merged_Claro_cambio_equipo_FTTH['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_cambio_equipo_FTTH['hora_inicio_call_center'] = df_merged_Claro_cambio_equipo_FTTH['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_cambio_equipo_FTTH['hora_fin_call_center'] = df_merged_Claro_cambio_equipo_FTTH['hora_fin_call_center'].apply(parse_fecha) 
#9. Claro_post_venta_empresa
    df_merged_Claro_post_venta_empresa['hora_inicio_contrata'] = df_merged_Claro_post_venta_empresa['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_post_venta_empresa['hora_inicio_call_center'] = df_merged_Claro_post_venta_empresa['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_post_venta_empresa['hora_fin_call_center'] = df_merged_Claro_post_venta_empresa['hora_fin_call_center'].apply(parse_fecha) 
#10. Claro_post_venta_FTTH
    df_merged_Claro_post_venta_FTTH['hora_inicio_contrata'] = df_merged_Claro_post_venta_FTTH['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_post_venta_FTTH['hora_inicio_call_center'] = df_merged_Claro_post_venta_FTTH['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_post_venta_FTTH['hora_fin_call_center'] = df_merged_Claro_post_venta_FTTH['hora_fin_call_center'].apply(parse_fecha) 
#11. Claro_post_venta_hfc
    df_merged_Claro_post_venta_hfc['hora_inicio_contrata'] = df_merged_Claro_post_venta_hfc['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_post_venta_hfc['hora_inicio_call_center'] = df_merged_Claro_post_venta_hfc['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_post_venta_hfc['hora_fin_call_center'] = df_merged_Claro_post_venta_hfc['hora_fin_call_center'].apply(parse_fecha)  
#12. Claro_Reenvio_De_Senal_HFC
    df_merged_Claro_Reenvio_De_Senal_HFC['hora_inicio_contrata'] = df_merged_Claro_Reenvio_De_Senal_HFC['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_Reenvio_De_Senal_HFC['hora_inicio_call_center'] = df_merged_Claro_Reenvio_De_Senal_HFC['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_Reenvio_De_Senal_HFC['hora_fin_call_center'] = df_merged_Claro_Reenvio_De_Senal_HFC['hora_fin_call_center'].apply(parse_fecha)  
#13. Claro_activacion_empresas
    df_merged_Claro_activacion_empresas['hora_inicio_contrata'] = df_merged_Claro_activacion_empresas['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_activacion_empresas['hora_inicio_call_center'] = df_merged_Claro_activacion_empresas['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_activacion_empresas['hora_fin_call_center'] = df_merged_Claro_activacion_empresas['hora_fin_call_center'].apply(parse_fecha)  
#14. Claro_cambio_equipo_HFC
    df_merged_Claro_cambio_equipo_HFC['hora_inicio_contrata'] = df_merged_Claro_cambio_equipo_HFC['hora_inicio_contrata'].apply(parse_fecha) 
    df_merged_Claro_cambio_equipo_HFC['hora_inicio_call_center'] = df_merged_Claro_cambio_equipo_HFC['hora_inicio_call_center'].apply(parse_fecha) 
    df_merged_Claro_cambio_equipo_HFC['hora_fin_call_center'] = df_merged_Claro_cambio_equipo_HFC['hora_fin_call_center'].apply(parse_fecha)


    with engine.connect() as connection:
        df_merged_Claro_mesh_detalle.to_sql('tblActivacionesMeshDetalleExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesMeshDetalleExcel.")
#-2-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_Plume_WIFI.to_sql('tblActivacionesPlumeWIFIExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesPlumeWIFIExcel.")
#-3-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_Activación_FTTH.to_sql('tblActivaciónFTTHExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivaciónFTTHExcel.")
#-4-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_activación_HFC.to_sql('tblActivaciónHFCExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivaciónHFCExcel.")
#-5-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_reenvio_de_señal_empresa_HFC.to_sql('tblActivacionesReenviodeSeñalEmpresaHFCExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesReenviodeSeñalEmpresaHFCExcel.")   
#-6-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_reenvio_de_señal_FTTH.to_sql('tblActivacionesReenviodeSeñalFTTHExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesReenviodeSeñalFTTHExcel.")
#-7-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_cambio_equipo_empresa.to_sql('tblActivacionesCambioEquipoEmpresaExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesCambioEquipoEmpresaExcel.")
#-8-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_cambio_equipo_FTTH.to_sql('tblActivacionesCambioEquipoFTTHExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesCambioEquipoFTTHExcel.")  
#-9-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_post_venta_empresa.to_sql('tblActivacionesPostVentaEmpresaExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesPostVentaEmpresaExcel.")
#-10-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_post_venta_FTTH.to_sql('tblActivacionesPostVentaFTTHExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesPostVentaFTTHExcel.")
#-11-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_post_venta_hfc.to_sql('tblActivacionesPostVentaHFCExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesPostVentaHFCExcel.")  
#-12-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_Reenvio_De_Senal_HFC.to_sql('tblActivacionesReenviodeSenalHFCExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesReenviodeSenalHFCExcel.")
#-13-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_activacion_empresas.to_sql('tblActivacionesEmpresasExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesEmpresaExcel.")
#-14-#####################################################################################################################
    with engine.connect() as connection:
        df_merged_Claro_cambio_equipo_HFC.to_sql('tblActivacionesCambioEquipoHFCExcel', con=connection, if_exists='append', index=False)
        connection.execute(text("COMMIT"))
    print("Datos cargados exitosamente en la base de datos tblActivacionesCambioEquipoHFCExcel.")   

    ##############################################################################################   

    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_f,)
        cursor.callproc('sp_Campaña_ActivacionesDetalle_rango', parametros)
        conexion.commit()
        logging.info("Procedimiento almacenado sp_Campaña_ActivacionesDetalle_rango ejecutado correctamente.")
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

