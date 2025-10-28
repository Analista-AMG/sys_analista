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

def parse_fecha(fecha_str):
    # Intentar diferentes formatos
    for fmt in ('%d/%m/%y %H:%M', '%d/%m/%Y %H:%M'):
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except ValueError:
            continue
    # Si ningún formato coincide, devolver NaT (Not a Time)
    return pd.NaT

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
