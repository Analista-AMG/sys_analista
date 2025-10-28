import pandas as pd
from Campañas.funcion import *
from conexion import *
from unidecode import unidecode
from collections import Counter
from datetime import datetime, date
from deep_translator import GoogleTranslator
import os
import locale
from sqlalchemy import create_engine,text,Table, MetaData
import logging
import pyodbc
from datetime import datetime, timedelta
from logger_config import get_logger_with_session
import warnings
import traceback
warnings.filterwarnings("ignore")

def Campaña_SaleSys_EstadoAgente1(fecha_inicio, fecha_fin):
    #logger = get_logger_with_session(session_id)
    #logger.info(f"Iniciando reporte desde {fecha_inicio} a {fecha_fin}")
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows
        except locale.Error:
            logging.warning("No se pudo establecer el locale en español. Se usará el predeterminado.")

    engine = conectar_bdCargaExcel()

    # Eliminar información de las tablas Excel
    tables = ["TblEstadoAgenteExcel"]
    with engine.connect() as connection:
        with connection.begin() as transaction:
            for table in tables:
                connection.execute(text(f"DELETE FROM {table}"))
                logging.info(f"Contenido eliminado de la tabla {table}")

    # Convertir strings de fechas
    fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dia_inicio = fecha_ini.day
    dia_fin = fecha_f.day
    año = fecha_f.year
    mes = fecha_f.month
    mesNombre = fecha_f.strftime("%B").capitalize()

    logging.info(f"Iniciando nueva ejecución para fechas: {fecha_inicio} a {fecha_fin}")

    # Procesar archivos delivery por día
    for dia in range(dia_inicio, dia_fin + 1):
        ruta_origen = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Estado Agente\{mesNombre}\EstadoAgente{dia:02d}.csv"
        if not os.path.exists(ruta_origen):
            logging.warning(f"Archivo Estado agente no encontrado para el día {dia}: {ruta_origen}")
            continue  # sigue con el siguiente día

        try:
            df = pd.read_csv(ruta_origen, sep=",")
            df['Hora inicio'] = pd.to_datetime(df['Hora inicio'])
            df['Hora fin'] = pd.to_datetime(df['Hora fin'])

            # Obtener la fecha de las columnas DATETIME
            df['fecha_inicio'] = df['Hora inicio'].dt.date
            df['fecha_fin'] = df['Hora fin'].dt.date

            # Asegurar que las fechas sean datetime
            df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])
            df['fecha_fin'] = pd.to_datetime(df['fecha_fin'], errors='coerce')  # para NaT

            # Ajustar 'Hora fin' si 'fecha_fin' es diferente o vacía
            df.loc[(df['fecha_fin'] != df['fecha_inicio']) | (df['fecha_fin'].isna()), 'Hora fin'] = df['Hora inicio']

            # Eliminar registros SOF - Sign Off consecutivos excepto el último
            for agente, grupo in df.groupby('Codigo del Agente'):
                indices_a_eliminar = []
                ultimo_sign_off = None

                for i in range(1, len(grupo)):
                    actual = grupo.iloc[i]
                    anterior = grupo.iloc[i - 1]

                    if actual['Funcion'] == 'SOF - Sign Off' and anterior['Funcion'] == 'SOF - Sign Off':
                        indices_a_eliminar.append(grupo.index[i - 1])
                    if actual['Funcion'] == 'SOF - Sign Off':
                        ultimo_sign_off = grupo.index[i]

                if indices_a_eliminar and ultimo_sign_off in indices_a_eliminar:
                    indices_a_eliminar.remove(ultimo_sign_off)

                df = df.drop(indices_a_eliminar)

            df = df.reset_index(drop=True)

            df_final = df.copy()

            # Ajustar 'Hora fin' para SOF y otros casos
            for agente, grupo in df_final.groupby('Codigo del Agente'):
                for i in range(1, len(grupo)):
                    registro_actual = grupo.iloc[i]

                    if registro_actual['Funcion'] == 'SOF - Sign Off':
                        registro_anterior = grupo.iloc[i - 1]

                        if i < len(grupo) - 1:
                            registro_siguiente = grupo.iloc[i + 1]
                            diferencia_tiempo = registro_siguiente['Hora inicio'] - registro_actual['Hora inicio']

                            if diferencia_tiempo <= pd.Timedelta(minutes=5):
                                df_final.at[grupo.index[i - 1], 'Hora fin'] = registro_siguiente['Hora inicio']
                            else:
                                df_final.at[grupo.index[i - 1], 'Hora fin'] = registro_actual['Hora inicio']
                    else:
                        if i > 0:
                            registro_anterior = grupo.iloc[i - 1]
                            df_final.at[grupo.index[i - 1], 'Hora fin'] = registro_actual['Hora inicio']

                # Caso último estado SOF - Sign Off
                if len(grupo) > 1 and grupo.iloc[-1]['Funcion'] == 'SOF - Sign Off':
                    df_final.at[grupo.index[-2], 'Hora fin'] = grupo.iloc[-1]['Hora inicio']

            df_final = df_final[df_final['Funcion'] != 'SOF - Sign Off'].reset_index(drop=True)

            df_final['Total estimado'] = df_final['Hora fin'] - df_final['Hora inicio']
            df_final['Total estimado'] = df_final['Total estimado'].astype(str).str.split().str[-1]

            fecha_frecuencia = df_final['fecha_inicio'].value_counts(normalize=True)

            fecha_mas_frecuente = fecha_frecuencia.idxmax() if not fecha_frecuencia.empty else None
            porcentaje_mas_frecuente = fecha_frecuencia.max() if not fecha_frecuencia.empty else 0

            if porcentaje_mas_frecuente >= 0.9:
                df_final = df_final[df_final['fecha_inicio'] == fecha_mas_frecuente]
            else:
                df_final = pd.DataFrame()
                logging.warning("No hay una fecha válida con al menos el 90% de coincidencia. Se eliminaron los registros.")

            columnas = ['Codigo del Agente', 'Agente', 'Funcion', 'Gestion', 'Hora inicio', 'Hora fin', 'Total estimado']
            df_to_sql = df_final[columnas]

            with engine.connect() as connection:
                df_to_sql.to_sql('TblEstadoAgenteExcel', con=connection, if_exists='append', index=False)
                connection.execute(text("COMMIT"))

            logging.info(f"Archivo Estado agente cargado exitosamente para el día {dia}: {ruta_origen}")

        except Exception as e:
            error_details = traceback.format_exc()
            logging.error(f"Error procesando archivo Estado agente {ruta_origen} para el día {dia}: {error_details}")

    # Ejecutar procedimiento almacenado
    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_EstadoagenteSalesys_rango', parametros)
        conexion.commit()
        logging.info("Procedimiento almacenado Sp_CampañaDelivery_Rango ejecutado correctamente.")
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Error en la ejecución del procedimiento almacenado: {error_details}")
        return f"Error en la obtención de datos: {error_details}"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()      

def Campaña_SaleSys_EstadoAgente2_Aghaso(fecha_inicio, fecha_fin):

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
    tables = ["TblEstadoAgenteVentasExcel"]

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
        ruta_Estado = fr"\\SRV-FS\AnalistaControlGestion\DESCARGA INFORMES\{año}\Aghaso\Estado Agente\{mesNombre}\EstadoagenteSS{dia:02d}.csv"
        #ruta_Estado = f'Z:\\DESCARGA INFORMES\\{año}\\Aghaso\\Estado Agente\\{mesNombre}\\EstadoagenteSS{dia}.csv'

        if os.path.exists(ruta_Estado):
            try:
                
                df = pd.read_csv(ruta_Estado,sep=",")

                df['Date'] = pd.to_datetime(df['Date'])
                df['Date end'] = pd.to_datetime(df['Date end'])

                df['fecha_inicio'] = df['Date'].dt.date
                df['fecha_fin'] = df['Date end'].dt.date

                df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])
                df['fecha_fin'] = pd.to_datetime(df['fecha_fin'], errors='coerce')  # Manejar valores vacíos (NaT)

                df.loc[(df['fecha_fin'] != df['fecha_inicio']) | (df['fecha_fin'].isna()), 'Date end'] = df['Date']

                for agente, grupo in df.groupby('Agent name'):
                    indices_a_eliminar = []  # Para almacenar los índices de los SOF consecutivos a eliminar
                    ultimo_sign_off = None  # Para almacenar el índice del último SOF consecutivo
                    
                    for i in range(1, len(grupo)):
                        registro_actual = grupo.iloc[i]
                        registro_anterior = grupo.iloc[i - 1]
                        
                        if registro_actual['Status'] == 'SOF - Sign Off':
                            if registro_anterior['Status'] == 'SOF - Sign Off':
                                # Marcar el anterior para eliminar
                                indices_a_eliminar.append(grupo.index[i - 1])
                            ultimo_sign_off = grupo.index[i]  # Guardar el índice del último SOF consecutivo
                    
                    if indices_a_eliminar:
                        if ultimo_sign_off in indices_a_eliminar:
                            indices_a_eliminar.remove(ultimo_sign_off)
                    
                    df = df.drop(indices_a_eliminar)

                df = df.reset_index(drop=True)

                df_final = df.copy()
                                    
                for agente, grupo in df_final.groupby('Agent name'):
                    for i in range(1, len(grupo)):
                        # Registro actual en el grupo
                        registro_actual = grupo.iloc[i]

                        if registro_actual['Status'] == 'SOF - Sign Off':
                            # Registro anterior
                            registro_anterior = grupo.iloc[i - 1]
                            
                            # Verificar si existe un siguiente registro para aplicar la lógica de los 5 minutos
                            if i < len(grupo) - 1:
                                registro_siguiente = grupo.iloc[i + 1]
                                
                                # Comparar la diferencia entre la Hora inicio del SOF - Sign Off y el siguiente registro
                                diferencia_tiempo = registro_siguiente['Date'] - registro_actual['Date']
                                
                                # Si la diferencia de tiempo es menor o igual a 5 minutos
                                if diferencia_tiempo <= pd.Timedelta(minutes=5):
                                    # Ajustar 'Hora fin' del registro anterior al 'Hora inicio' del registro siguiente
                                    df_final.at[grupo.index[i - 1], 'Date end'] = registro_siguiente['Date']
                                else:
                                    # Si la diferencia de tiempo es mayor a 5 minutos, ajustar 'Hora fin' del registro anterior con la 'Hora fin' del registro actual
                                    df_final.at[grupo.index[i - 1], 'Date end'] = registro_actual['Date']                
                        
                        # Ajuste en caso de que no haya SOF - Sign Off
                        else:
                            if i > 0:  # Evitar índice fuera de rango
                                registro_anterior = grupo.iloc[i - 1]
                                # Ajustar 'Hora fin' del registro anterior al 'Hora inicio' del registro actual
                                df_final.at[grupo.index[i - 1], 'Date end'] = registro_actual['Date']

                    # Caso donde el SOF - Sign Off es el último estado de un asesor
                    if len(grupo) > 1 and grupo.iloc[-1]['Status'] == 'SOF - Sign Off':
                        df_final.at[grupo.index[-2], 'Date end'] = grupo.iloc[-1]['Date']

                # Filtrar los registros de 'SOF - Sign Off'
                df_final = df_final[df_final['Status'] != 'SOF - Sign Off'].reset_index(drop=True)

                # Aplicar una operación entre columnas solo a las filas que cumplen la condición
                df_final['Time total'] = df_final['Date end'] - df_final['Date']  # Ejemplo de suma entre dos columnas
                df_final['Time total'] = df_final['Time total'].astype(str).str.split().str[-1]

                # Paso 1: Contar la frecuencia de cada fecha en 'fecha_inicio'
                fecha_frecuencia = df_final['fecha_inicio'].value_counts(normalize=True)

                # Paso 2: Verificar si la frecuencia más alta es mayor o igual al 90%
                fecha_mas_frecuente = fecha_frecuencia.idxmax()
                porcentaje_mas_frecuente = fecha_frecuencia.max()

                if porcentaje_mas_frecuente >= 0.9:
                    # Paso 3: Si cumple con el 90%, filtrar los registros con esa fecha
                    df_final = df_final[df_final['fecha_inicio'] == fecha_mas_frecuente]
                else:
                    # Paso 4: Si no cumple, eliminar todos los registros
                    df_final = pd.DataFrame()  # O eliminar las filas que no cumplen
                    logging.warning("⚠️ No hay una fecha válida con al menos el 90% de coincidencia. Se eliminaron los registros.")
                columnas = ['Status','Date','Date end','Time total','Agent name']
                df_to_sql = df_final[columnas]

                fecha_actual = datetime.now()
                

                with engine.connect() as connection:
                    df_to_sql.to_sql('TblEstadoAgenteVentasExcel', con=connection, if_exists='append', index=False)
                    connection.execute(text("COMMIT"))

                logging.info(f"Archivo Estado agente cargado exitosamente para el día {dia}: {ruta_Estado}")
            except Exception as e:
                logging.error(f"Error procesando archivo Estado agente {ruta_Estado} para el día {dia}: {e}")
        else:
            logging.warning(f"Archivo Estado agente no encontrado para el día {dia}: {ruta_Estado}")

    conexion = conectar_bdStores()
    try:
        cursor = conexion.cursor()
        parametros = (fecha_ini, fecha_f)
        cursor.callproc('Sp_EstadoagenteSalesysAghaso_rango', parametros)
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
