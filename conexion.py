import pymssql
import pymysql
import mysql.connector
import pyodbc
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def conectar_odbc():
    servidor = '192.168.16.103'
    nombre_base_datos = 'BD_AMG'
    usuario = 'sqladmin'
    contraseña = '#contraAdmin2159xD'
    driver = '{ODBC Driver 17 for SQL Server}'  # Asegúrate que esté instalado
    return f'DRIVER={driver};SERVER={servidor};DATABASE={nombre_base_datos};UID={usuario};PWD={contraseña}'

def conectar_login():
    servidor = '192.168.16.103'
    nombre_base_datos = 'BD_AMG'
    usuario = 'sqladmin'
    contraseña = '#contraAdmin2159xD'

    connection_string = (
        f"mssql+pyodbc://{usuario}:{contraseña}@{servidor}/{nombre_base_datos}"
        f"?driver=ODBC%20Driver%2017%20for%20SQL%20Server"
    )
    return connection_string

def conectar_login_odbc():
    return (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=192.168.16.103;"
        "DATABASE=BD_AMG;"
        "UID=sqladmin;"
        "PWD=#contraAdmin2159xD;"
    )

def conectar_bdCargaExcel():

    servidor = '192.168.16.103'
    nombre_base_datos = 'BD_AMG'
    usuario = 'sqladmin' #
    contraseña = '#contraAdmin2159xD'

    connection_string = f'mssql+pyodbc://{usuario}:{contraseña}@{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server'

    # Crear y devolver el engine
    engine = create_engine(connection_string)

    return engine


def conectar_bdStores():
    try:
        conn = pymssql.connect(
            server='192.168.16.103',
            user='sqladmin',#
            password='#contraAdmin2159xD',#
            database='BD_AMG',
            as_dict=True
        )
        print("Conexión exitosa.")
        return conn
    except pymssql.Error as e:
        print(f"Error de conexión: {e}")
        return None


    
def conectar_bdStores_Navicat():
    try:
        conn = pymysql.connect(
        host='172.19.112.169',
        user='E8323824', 
        password='1Cc19evQmRhy2Noo',
        database='hfc_Programacion'
        )
        print("Conexión exitosa.")
        return conn
    except pymssql.Error as e:
        print(f"Error de conexión: {e}")
        return None


def conectar_bdStores_Intranet():
    try:
        conn = pymysql.connect(
        host='192.168.16.111',
        user='analista', 
        password='V1aR&n$mf31!',
        database='intranet'
        )
        print("Conexión exitosa.")
        return conn
    except pymssql.Error as e:
        print(f"Error de conexión: {e}")
        return None


    
def conectar_bdStores_MesaSoporte():
    try:
        conn = pymysql.connect(
                host="172.19.112.169",
                port=3306,
                user="E8324761",
                password="sWVg67zVALu8Fdrc",
                database="hfc",
                connect_timeout=5  # Timeout en segundos
            )
        print("Conexión exitosa.")
        return conn
    except pymssql.Error as e:
        print(f"Error de conexión: {e}")
        return None


def conectar_bdStores_MultiSkill():
    try:
        conn = pymysql.connect(
                host="172.19.112.169",
                port=3306,
                user="E8323593",
                password="KgBuyT7p216DFjq1",
                database="hfc",
                connect_timeout=5  # Timeout en segundos
            )
        print("Conexión exitosa.")
        return conn
    except pymssql.Error as e:
        print(f"Error de conexión: {e}")
        return None

def conectar_bdStores_Navicat2():
    try:
        conn = pymysql.connect(
                host="172.19.112.169",
                port=3306,
                user="E8324761",
                password="sWVg67zVALu8Fdrc",
                database="hfc",
                connect_timeout=5  # Timeout en segundos
            )
        print("Conexión exitosa.")
        return conn
    except pymssql.Error as e:
        print(f"Error de conexión: {e}")
        return None



def conectar_bdStores_Navicat_SQL():
    try:
        conn = pymssql.connect(
            server='192.168.16.103',  # Dirección del servidor SQL Server
            user='sqladmin',  # Usuario de la base de datos SQL Server 
            password='#contraAdmin2159xD',  # Contraseña del usuario 
            database='BD_AMG'
        )
        print("Conexión exitosa.")
        return conn
    except pymssql.Error as e:
        print(f"Error de conexión: {e}")
        return None
