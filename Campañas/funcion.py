import os
import pandas as pd
import numpy as np
from unidecode import unidecode
from datetime import datetime, date
import re
import pandas as pd
import re
from unidecode import unidecode
from sqlalchemy import create_engine

### FUNCIONES APLICADAS A LOS REPORTES S/P FIJA

# Normalización de los nombres de columnas
def normalize_column_name(col):
    col = unidecode(col)
    col = col.strip().lower().replace(' ', '_')
    return col

def normalize_name(name):
    if pd.isnull(name):
        return None
    # Elimina tildes y diacríticos
    name = unidecode(name)
    name = name.strip().lower()
    # Reemplazar múltiples espacios con un solo espacio
    name = re.sub(r'\s+', ' ', name)
    return name
  
# Función para extraer apellidos y primer nombre en una sola columna y en mayúsculas
def extraer_apellidos_primer_nombre(nombre_completo):

    nombre_completo = nombre_completo.upper()  # Convertir a mayúsculas
    primer_espacio = nombre_completo.find(' ')  # Encontrar el primer espacio
    segundo_espacio = nombre_completo[primer_espacio + 1:].find(' ') + primer_espacio + 1  # Encontrar el segundo espacio
    
    apellidos = nombre_completo[segundo_espacio + 1:]  # Apellidos son todo después del segundo espacio
    primer_nombre = nombre_completo[:primer_espacio]  # Primer nombre es todo antes del primer espacio
    return f"{primer_nombre} {apellidos}"

# Función para normalizar el texto en una columna
def normalizar_texto(df, columna):
    # Reemplazar múltiples espacios con un solo espacio
    df[columna] = df[columna].str.replace(r'\s+', ' ', regex=True)
    df[columna] = df[columna].str.strip()
    return df

def conectar_bd(servidor, nombre_base_datos, usuario, contraseña):
    connection_string = f'mssql+pyodbc://{usuario}:{contraseña}@{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    #print('Conexión exitosa')
    return engine

def ajustar_tiempo_seg(row):
    if row['condicion'] == 'FULL TIME':
        if row['comida'] < 0.75:
            ajuste = 0.75 - row['comida']
            nueva_cola = row['en_la_cola'] - (ajuste + 0.25)
        else:
            nueva_cola = row['en_la_cola']
        # Limitar el valor máximo de la cola a 9.5 para FULL TIME
        nueva_cola = min(nueva_cola, 9.5)
    elif row['condicion'] == 'PART TIME':
        # Limitar el valor máximo de la cola a 6.00 para PART TIME
        nueva_cola = min(row['en_la_cola'], 6.00)
    else:
        nueva_cola = row['en_la_cola']
    # Asegurarse de que nueva_cola no sea menor que 0
    nueva_cola = max(nueva_cola, 0)
    return nueva_cola

def ajustar_tiempo_seg_2(row):
    if row['condicion'] == 'FULL TIME':
        if row['comida'] < 2700:
            ajuste = 2700 - row['comida']
            nueva_cola = row['en_la_cola'] - (ajuste + 900)
        else:
            nueva_cola = row['en_la_cola']
        # Limitar el valor máximo de la cola a 9.5 para FULL TIME
        nueva_cola = min(nueva_cola, 34200)
    elif row['condicion'] == 'PART TIME':
        # Limitar el valor máximo de la cola a 6.00 para PART TIME
        nueva_cola = min(row['en_la_cola'], 21600)
    else:
        nueva_cola = row['en_la_cola']
    # Asegurarse de que nueva_cola no sea menor que 0
    nueva_cola = max(nueva_cola, 0)
    return nueva_cola

# Obtener la fecha actual y el periodo
fecha_actual = pd.to_datetime("now")
fecha_menos_1 = fecha_actual.date() - pd.Timedelta(days=1) # Día anterior
year = fecha_menos_1.year
mes = fecha_menos_1.month
mes_name = fecha_menos_1.strftime('%B')

# Definir el rango de fechas para el mes anterior
inicio_periodo = pd.to_datetime(f"{year}-{mes}-01").date() # Primer día del mes anterior
fin_periodo =  fecha_menos_1 # Último día que sería el día anterior
fechas_esperadas = pd.date_range(start=inicio_periodo, end=fin_periodo, freq='D').date

# Función para validar que todas las fechas estén en el DataFrame
def validar_fechas(df, columna_fecha, bd):

    # Obtener las fechas únicas en el DataFrame
    fechas_presentes = df[columna_fecha].dropna().unique()
    fechas_faltantes = set(fechas_esperadas) - set(fechas_presentes)
    fechas_extra = set(fechas_presentes) - set(fechas_esperadas)

    # Convertir los sets a listas y ordenarlas
    fechas_faltantes = sorted(list(fechas_faltantes))
    fechas_extra = sorted(list(fechas_extra))

    # Ver si hay fechas faltantes o fechas extras y mostrar el texto limpio
    if len(fechas_faltantes) > 0:
        print(f"{bd}, faltan las siguientes fechas: {'| '.join(map(str, fechas_faltantes))}, actualizado hasta: {fechas_presentes.max()}.")
    if len(fechas_extra) > 0:
        print(f"{bd}, hay fechas adicionales: {'| '.join(map(str, fechas_extra))}.")
    
    # Si todo está completo
    if len(fechas_faltantes) == 0 and len(fechas_extra) == 0:
        print(f"{bd}, periodo {year}-{mes} fechas completas hasta: {fechas_esperadas.max()}.")
    
    # Devolver si el DataFrame tiene todas las fechas
    return len(fechas_faltantes) == 0

# Función para comparar las fechas de las columnas 'fechas_faltantes' y 'fecha_sin_gestion'
def compare_dates(row):
    if pd.notna(row['fechas_faltantes']):
        fechas_sin_gestion = row['fecha_sin_gestion'].split('|') if pd.notna(row['fecha_sin_gestion']) else []
        fechas_faltantes = row['fechas_faltantes'].split('|')
        fechas_restantes = [fecha for fecha in fechas_faltantes if fecha not in fechas_sin_gestion]
        return '|'.join(fechas_restantes) if fechas_restantes else None
    return row['fecha_sin_gestion']


def check_and_concatenate_csv_files(folder_path, file_extension='.csv', sep=';'):
    # Obtener la lista de archivos CSV en la carpeta
    files = [file for file in os.listdir(folder_path) if file.endswith(file_extension)]
    
    # Leer el primer archivo para obtener la estructura de columnas de referencia
    reference_file_path = os.path.join(folder_path, files[0])
    df_reference = pd.read_csv(reference_file_path, sep=sep)
    
    # Crear listas y diccionario para almacenar resultados
    dataframes = []
    problematic_files = {}

    # Iterar sobre cada archivo CSV
    for file in files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, sep=sep)
        
        # Verificar la estructura de columnas del archivo actual con el de referencia
        if set(df.columns) != set(df_reference.columns):
            print(f"Advertencia: El archivo {file} tiene una estructura de columnas diferente.")
            problematic_files[file] = "Estructura de columnas diferente"
        else:
            # Verificar si el orden de las columnas es diferente al de referencia
            if not df.columns.equals(df_reference.columns):
                print(f"Advertencia: El archivo {file} tiene las columnas en distinto orden.")
                problematic_files[file] = "Orden de columnas diferente"
            else:
                dataframes.append(df)
    
    # Si no hay archivos con problemas, concatenar los DataFrames en uno solo
    if not problematic_files:
        df_merge = pd.concat(dataframes, ignore_index=True)
        print("Todos los archivos tienen la misma estructura de columnas y orden. Concatenación exitosa.")
        return df_merge
    else:
        print("No se puede realizar la concatenación debido a problemas en la estructura de columnas de los siguientes archivos:")
        for file, issue in problematic_files.items():
            print(f"- {file}: {issue}")
        return None

# Normalización de los nombres de columnas


def normalize_column_name(col):
    # Convertir cualquier valor a string antes de aplicar unidecode
    col = str(col)  # Asegurarse de que sea un string
    col = unidecode(col)  # Elimina tildes y diacríticos
    col = col.strip().lower().replace(" ", "_").replace('/', '_')  # Normalización adicional
    return col


# Normalización de los nombres de columnas
def normalize_column_name_point(col):
    col = unidecode(col)  # Elimina tildes y diacríticos
    col = col.strip().lower().replace('.', '')
    return col

# Función para dividir la cadena por la primera coma
def split_asesor(row):
    parts = row['asesor'].split(',', 1)
    if len(parts) > 1:
        return parts[0].strip(), parts[1].strip()
    else:
        return parts[0].strip(), None
    

def parse_fecha(fecha_str):
    # Intentar diferentes formatos
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S','%d/%m/%y %H:%M', '%d/%m/%Y %H:%M'):
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except ValueError:
            continue
    # Si ningún formato coincide, devolver NaT (Not a Time)
    return pd.NaT

def parse_fecha_genesys(fecha_str):
    # Intentar diferentes formatos
    for fmt in ('%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M', '%d/%m/%y %H:%M'):
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except ValueError:
            continue
    # Si ningún formato coincide, devolver NaT (Not a Time)
    return pd.NaT

def parse_fecha_corpo(fecha_str):
    # Intentar diferentes formatos
    for fmt in ('%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M', '%d/%m/%y %H:%M'):
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except ValueError:
            continue
    # Si ningún formato coincide, devolver NaT (Not a Time)
    return pd.NaT

def parse_fecha_laraigo(fecha_str):
    # Intentar diferentes formatos
    for fmt in ('%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d/%m/%y %H:%M:%S'):
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except ValueError:
            continue
    # Si ningún formato coincide, devolver NaT (Not a Time)
    return pd.NaT


def parse_fecha_Activaciones(fecha_str):
    # Intentar diferentes formatos
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S'):
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except ValueError:
            continue
    # Si ningún formato coincide, devolver NaT (Not a Time)
    return pd.NaT

def parse_fecha_TOA(fecha_str):
    # Intentar diferentes formatos
    for fmt in ('%d/%m/%Y', '%d/%m/%y'):
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except ValueError:
            continue
    # Si ningún formato coincide, devolver NaT (Not a Time)
    return pd.NaT



###################################################
##PARA ACTIVACIONES OCUPACION #############
def log_subprocess(msg):
    """Función de logging optimizada para subprocess"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_msg = f"[{timestamp}] [OCUPACION] {msg}"
    print(formatted_msg, flush=True)

def normalize_column_name_acti(col_name):
    """Normalizar nombres de columnas"""
    return col_name.lower().replace(' ', '_').replace('-', '_')

def generar_tiempos_por_franja(df_agentes, df_franjas):
    """Generar tiempos por franja para los agentes"""
    resultados = []

    for _, agente_row in df_agentes.iterrows():
        agente_inicio = agente_row['hora_inicio']
        agente_fin = agente_row['hora_fin']
        agente_fecha = agente_inicio.date()
        codigo_salesys = agente_row['codigo_salesys']
        agente_funcion = agente_row['funcion']

        # Filtrar franjas por la fecha del agente
        franjas_fecha = df_franjas[(df_franjas['fecha_hora_inicio'].dt.date == agente_fecha)]

        for _, franja_row in franjas_fecha.iterrows():
            franja_inicio = franja_row['fecha_hora_inicio']
            franja_fin = franja_row['fecha_hora_fin']
            etiqueta_franja = franja_row['etiqueta_franja']

            # Encontrar la intersección entre el intervalo del agente y la franja
            interseccion_inicio = max(agente_inicio, franja_inicio)
            interseccion_fin = min(agente_fin, franja_fin)

            if interseccion_inicio < interseccion_fin:
                # Calcular la duración en segundos
                duracion_segundos = (interseccion_fin - interseccion_inicio).total_seconds()

                resultados.append({
                    'codigo_salesys': codigo_salesys,
                    'funcion': agente_funcion,
                    'fecha': agente_fecha,
                    'franja': etiqueta_franja,
                    'tiempo_segundos': duracion_segundos
               })

    return pd.DataFrame(resultados)

def mapear_segundos_por_franja(df_gestiones, df_franjas):
    """Función para dividir gestiones por franjas y calcular tiempo en cada una"""
    registros = []

    for index, row in df_gestiones.iterrows():
        hora_inicio = row['hora_inicio_call_center']
        hora_fin = row['hora_fin_call_center']

        # Filtrar franjas que intersectan con la gestión
        franjas_intersectadas = df_franjas[(df_franjas['fecha_hora_inicio'] < hora_fin) & (df_franjas['fecha_hora_fin'] > hora_inicio)]

        for _, franja in franjas_intersectadas.iterrows():
            inicio_franja = max(hora_inicio, franja['fecha_hora_inicio'])
            fin_franja = min(hora_fin, franja['fecha_hora_fin'])
            tiempo_segundos = (fin_franja - inicio_franja).total_seconds()

            registros.append({
                'codigo_salesys': row['codigo_salesys'],
                'fecha': hora_inicio.date(),
                'franja': franja['etiqueta_franja'],
                'tiempo_segundos': tiempo_segundos
            })

    return pd.DataFrame(registros)


def log_subprocess(msg):
    """Función de logging optimizada para subprocess"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_msg = f"[{timestamp}] [AVERIAS] {msg}"
    print(formatted_msg, flush=True)

def timedelta_to_hms(tdelta):
    """Función para convertir timedelta a formato 'hh:mm:ss'"""
    total_seconds = tdelta.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"