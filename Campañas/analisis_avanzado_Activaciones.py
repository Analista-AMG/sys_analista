import os
import sqlalchemy
from sqlalchemy import create_engine, text, Table, MetaData
import pyodbc
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import matplotlib.pyplot as plt  # Nuevo import
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
from Campañas.functions_Activaciones import *

def analizar_casos(fecha_final, incluir_domingos):
    # CONEXION A LA BD
    servidor = '192.168.16.103'
    nombre_base_datos = 'BD_AMG'
    usuario = ''
    contraseña = ''
    connection_string = f'mssql+pyodbc://{usuario}:{contraseña}@{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)

    # Cargar la base activ que tiene los tickets
    with engine.connect() as connection:
        df_activ = pd.read_sql(fr""" SELECT 
          [fecha_filtro] AS fecha
          ,[producto]
          ,[caso]
          ,[hora_inicio_contrata]
          ,[hora_inicio_call_center]
          ,[hora_fin_call_center]
          ,[rango_30min]
          ,[tmo_averia] AS averia
          ,[objtmg<720seg] AS ns_720
          ,[estado1] AS estado
      FROM [BD_AMG].[dbo].[TblActivacionesBD]
      WHERE 
      fecha_filtro >= '2025-03-01' AND fecha_filtro <= '{fecha_final}'
      AND
      caso in ('ACTIVACION EMPRESA', 'ACTIVACION FTTH', 'ACTIVACION HFC', 'CAMBIO EQUIPO EMPRESA', 'CAMBIO EQUIPO FTTH', 'CAMBIO EQUIPO HFC', 'PLUME WIFI ACTIVACION', 'POST VENTA EMPRESA', 'POST VENTA FTTH', 'POST VENTA HFC', 'REENVIO DE SENAL HFC', 'REENVIO SENAL EMPRESA', 'REENVIO SENAL FTTH', 'REGISTRO MESH')
      AND
      tmo_averia = 0
    """, con=connection)
        
    df_activ['fecha'] = pd.to_datetime(df_activ['fecha'])
    df_activ['rango_30min'] = df_activ['rango_30min'].astype(str)

    # Filtrar según el parámetro
    df_activv_con_domingos = df_activ[(df_activ['fecha'].dt.weekday == 6) & (df_activ['producto'] != 'EMPRESA')]
    df_activv_sin_domingos = df_activ[(df_activ['fecha'].dt.weekday != 6) & (df_activ['producto'] != 'EMPRESA')]

    if incluir_domingos:
        df_base = df_activv_con_domingos
    else:
        df_base = df_activv_sin_domingos

    df = df_base

    # ————— PREPARACIÓN DE DATOS —————
    df['fecha'] = pd.to_datetime(df['fecha'])
    ultimo     = df['fecha'].max()
    fecha_str  = ultimo.strftime('%Y-%m-%d')

    df_hist = df[df['fecha'] < ultimo]
    df_ult  = df[df['fecha'] == ultimo]

    # 1) Franjas a mostrar: todas las del último día
    franjas = sorted(df_ult['rango_30min'].unique())
    labs     = [f[:5] for f in franjas]

    # 2) NS general por franja
    ns_general = (
        df_ult
          .groupby('rango_30min')['ns_720']
          .mean()
          .reindex(franjas, fill_value=np.nan)
          .values
    )

    # 3) Histórico promedio y último conteo
    hist = (
        df_hist
          .groupby(['producto','caso','rango_30min','fecha'])
          .size()
          .reset_index(name='cnt')
    )
    hist_avg = (
        hist
          .groupby(['producto','caso','rango_30min'])['cnt']
          .mean()
          .reset_index(name='hist_avg')
    )
    ult_cnt = (
        df_ult
          .groupby(['producto','caso','rango_30min'])
          .size()
          .reset_index(name='ult_cnt')
    )

    metrics = (
        hist_avg
          .merge(ult_cnt, on=['producto','caso','rango_30min'], how='outer')
          .fillna({'hist_avg':0,'ult_cnt':0})
    )
    metrics['pct_diff'] = np.where(
        metrics['hist_avg'] > 0,
        (metrics['ult_cnt'] - metrics['hist_avg']) / metrics['hist_avg'] * 100,
        np.nan
    )

    # 4) Pivot para lookup rápido
    df_pct     = metrics.pivot(index=['producto','caso'], columns='rango_30min', values='pct_diff')
    df_histavg = metrics.pivot(index=['producto','caso'], columns='rango_30min', values='hist_avg')
    df_ultcnt  = metrics.pivot(index=['producto','caso'], columns='rango_30min', values='ult_cnt')

    # Productos y casos
    productos = df_ult['producto'].unique().tolist()
    prod_casos = {
        p: df_ult[df_ult['producto']==p]['caso'].unique().tolist()
        for p in productos
    }

    # 5) Construir etiquetas de fila
    row_labels = ['NIVEL DE SERVICIO'] + [
        f"{caso}"
        for prod in productos
        for caso in prod_casos[prod]
    ]
    n_rows = len(row_labels)

    # 7) Rellenar valores
    cell_values = []

    for j, fr in enumerate(franjas):
        texts = []
        # NS general
        ns = ns_general[j]
        if not np.isnan(ns):
            texts.append(f"{ns*100:.0f}%")
        else:
            texts.append("")
        # Cada caso: mostramos "último/histórico"
        for prod in productos:
            for caso in prod_casos[prod]:
                v_pct = df_pct.at[(prod,caso), fr] if (prod,caso) in df_pct.index else np.nan
                h_avg = df_histavg.at[(prod,caso), fr] if (prod,caso) in df_histavg.index else 0
                u_cnt = df_ultcnt.at[(prod,caso), fr] if (prod,caso) in df_ultcnt.index else 0
                if np.isnan(v_pct):
                    texts.append("")
                else:
                    texts.append(f"{int(u_cnt)}/{h_avg:.1f}")
        cell_values.append(texts)

    # 8) Ensamblar la tabla para matplotlib
    # Transponer para matplotlib (matplotlib espera filas)
    table_data = list(map(list, zip(*([row_labels] + cell_values))))
    column_headers = ['SKILLS'] + labs

    # Guardar imagen con matplotlib
    servidor = "SERVIDOR06"
    carpeta = "web"
    subcarpeta = "static"
    output_dir = rf"\\{servidor}\python\{carpeta}\{subcarpeta}"

    output_path = os.path.join(output_dir, "activaciones_result.png")
    if not os.path.exists(output_dir):
        print(f"La ruta de red {output_dir} no existe o no es accesible. Guardando localmente.")
        output_dir = r"v:\web\static"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "activaciones_result.png")

    fig, ax = plt.subplots(figsize=(18, 6))
    ax.axis('off')
    tabla = ax.table(
        cellText=table_data,
        colLabels=column_headers,
        loc='center',
        cellLoc='center'
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 1.5)
    plt.title(f"CASOS APK SALESYS — NS en cada franja y el incremento de casos — Día comparado {fecha_str} frente al histórico", fontsize=16)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Imagen guardada en: {output_path}")

# Ejemplo de uso:
#analizar_casos('2025-08-19', True)