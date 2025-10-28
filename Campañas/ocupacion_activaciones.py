import pandas as pd
import sys
import os
import sqlalchemy
from Campañas.funcion import *
from sqlalchemy import create_engine, text, Table, MetaData
from conexion import *
import pyodbc
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def procesar_ocupacion(fecha_inicio, fecha_fin):
    """
    Procesar ocupación de activaciones para un rango de fechas
    Args:
        fecha_inicio (str): Fecha de inicio en formato 'YYYY-MM-DD'
        fecha_fin (str): Fecha de fin en formato 'YYYY-MM-DD'
    """
    try:
        log_subprocess(f"🚀 Iniciando procesamiento de ocupación desde {fecha_inicio} hasta {fecha_fin}")

      
        # Conectar a la base de datos

        engine = conectar_bdCargaExcel()
        # Generar lista de fechas en el rango
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')

        current_date = fecha_inicio_dt
        fechas_procesadas = 0

        while current_date <= fecha_fin_dt:
            fecha_str = current_date.strftime('%Y-%m-%d')
            log_subprocess(f"📅 Procesando fecha: {fecha_str}")

            try:
                # Leer datos desde la base de datos
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

                if df.empty:
                    log_subprocess(f"⚠️ No hay datos de activaciones para {fecha_str}")
                    current_date += timedelta(days=1)
                    continue

                # Procesar datos
                df_activaciones = df.copy()
                df_estado_agente = df_2.copy()
                franjas = df_Franjas.copy()
                df_nomina = df_3.copy()

                # Normalizar franjas
                franjas['Fecha_Hora_Inicio'] = pd.to_datetime(franjas['Fecha_Hora_Inicio'], format='%d-%m-%Y %H:%M:%S')
                franjas['Fecha_Hora_Fin'] = pd.to_datetime(franjas['Fecha_Hora_Fin'], format='%d-%m-%Y %H:%M:%S')
                franjas.columns = [normalize_column_name(col) for col in franjas.columns]

                # Convertir tipos de datos
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

                # Eliminar registros existentes de la misma fecha
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
                log_subprocess(f"❌ Error procesando fecha {fecha_str}: {e}")

            current_date += timedelta(days=1)

        log_subprocess(f"🎯 Procesamiento completado: {fechas_procesadas} fechas procesadas exitosamente")
        return True

    except Exception as e:
        log_subprocess(f"❌ Error general en procesamiento: {e}")
        return False


