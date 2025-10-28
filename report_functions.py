from Campañas.delivery import *
from Campañas.EstadoSalesys import *
from flask import request
from Campañas.Genesys import *
from Campañas.aghaso import *
from Campañas.MultiSkill import *
from Campañas.Alambrico import *
from Campañas.Validaciones import *
from Campañas.Corporativo import *
from Campañas.MesaAyuda import *
from Campañas.Inalambrico import *
from Campañas.Activaciones import *
from Campañas.MesaSoporte import *
from Campañas.SVFF import *
from Campañas.Seguimiento import *
import os
####################################################################################################################################
##--> Salesys -------------------------------------------------------------------
def SaleSys_report_1(start_date, end_date):   
    Campaña_SaleSys_EstadoAgente1(start_date, end_date)
    return f"Reporte Salesys ejecutado correctamente de {start_date} al {end_date}"

def SaleSys_report_2(start_date, end_date):
    Campaña_SaleSys_EstadoAgente2_Aghaso(start_date, end_date)
    return f"Reporte Salesys ejecutado correctamente de {start_date} al {end_date}"

####################################################################################################################################
##--> AGHASO -------------------------------------------------------------------
def SaleSys_Aghaso_1(start_date, end_date):
    Campaña_Aghaso(start_date, end_date)
    return f"Reporte Salesys ejecutado correctamente de {start_date} al {end_date}"

def SaleSys_Aghaso_nomina(end_date):
    CargaNominaAghaso(end_date)
    return f"Reporte Salesys ejecutado correctamente del {end_date}"

def Aghaso_Kpi(end_date):
    KpiAghaso(end_date)
    return f"Reporte Salesys ejecutado correctamente del {end_date}"
####################################################################################################################################
##--> GENESYS
def Genesys_report_General(start_date, end_date):
    Campaña_Genesys_General(start_date, end_date)
    return f"Reporte Salesys ejecutado correctamente de {start_date} al {end_date}"

####################################################################################################################################
##--> Delivery
def delivery_report_1(start_date, end_date):
    Campaña_Delivery(start_date, end_date)
    return f"Reporte Delivery ejecutado correctamente de {start_date} al {end_date}"

def delivery_report_Nomina(end_date):
    CargaNominaDeliveryBioMensajeriaSoporte(end_date,)
    return f"Reporte Delivery ejecutado correctamente al {end_date}"

def delivery_report_Nomina_seg(end_date):
    CargaNominaDeliverySeguimiento(end_date,)
    return f"Reporte Delivery ejecutado correctamente al {end_date}"

def delivery_Kpi(end_date):
    KpiDelivery(end_date,)
    return f"Reporte Delivery ejecutado correctamente al {end_date}"

def delivery_Auditoria(end_date):
    Campaña_Delivery_Auditoria(end_date,)
    return f"Reporte Delivery ejecutado correctamente al {end_date}"

def delivery_Detallado(start_date, end_date):
    Campaña_Delivery_Detallado(start_date, end_date)
    return f"Reporte Delivery ejecutado correctamente de {start_date} al {end_date}"

####################################################################################################################################
##--> mULTISKILL 
def Multiskill_report_Nomina(end_date):
    CargaNominaMultiskill(end_date,)
    return f"Reporte Multiskill ejecutado correctamente al {end_date}"

def Multiskill_report_1(start_date, end_date):
    Campaña_Multiskill(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

def Multiskill_Kpi(end_date):
    KpiMultiskill(end_date,)
    return f"Reporte Multiskill ejecutado correctamente al {end_date}"

def Laraigo_Multiskill_report(start_date, end_date):
    Laraigo_Multiskill(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

def Interaccione_Multiskill_report(start_date, end_date):
    Interacciones_Multiskill(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

def Navicat_Multiskill_report(start_date, end_date):
    Campaña_Multiskill_Navicat(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

def Navicat_Multiskill_report_2(start_date, end_date):
    Campaña_Multiskill_Navicat_2(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

def Navicat_Multiskill_report_3(start_date, end_date):
    Campaña_Multiskill_Navicat_3(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

def Tardanzas_Multiskill_report(start_date, end_date):
    TardanzasMultiskill(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

def Validaciones_tickets_report(start_date, end_date):
    Validacionestickets(start_date, end_date)
    return f"Reporte Multiskill ejecutado correctamente de {start_date} al {end_date}"

####################################################################################################################################
##--> ALAMBRICO 

def Validacion_report_Nomina(end_date):
    CargaNominaValidacion(end_date,)
    return f"Reporte Validaciones ejecutado correctamente al {end_date}"

def Validaciones_report_1(start_date, end_date):
    Campaña_Validaciones(start_date, end_date)
    return f"Reporte Validaciones ejecutado correctamente de {start_date} al {end_date}"

def Validaciones_otros_report_1(start_date, end_date):
    Campaña_Validaciones_otros(start_date, end_date)
    return f"Reporte Validaciones ejecutado correctamente de {start_date} al {end_date}"

def Validaciones_Kpi(end_date):
    KpiValidaciones(end_date,)
    return f"Reporte Validaciones ejecutado correctamente al {end_date}"

def Validaciones_Interacciones_report(start_date, end_date):
    Interacciones_Validaciones(start_date, end_date)
    return f"Reporte Interacciones ejecutado correctamente de {start_date} al {end_date}"

def Validacion_Remota_navicat_report(start_date, end_date):
    Validacion_Remota_navicat(start_date, end_date)
    return f"Reporte Interacciones ejecutado correctamente de {start_date} al {end_date}"

def Encuesta_Detalle_navicat_report(start_date, end_date):
    Encuesta_Detalle_navicat(start_date, end_date)
    return f"Reporte Interacciones ejecutado correctamente de {start_date} al {end_date}"


####################################################################################################################################
##--> ALAMBRICO  
def Alambrico_report_Nomina(end_date):
    CargaNominaAlambrico(end_date,)
    return f"Reporte Alambrico ejecutado correctamente al {end_date}"

def Alambrico_report_1(start_date, end_date):
    Campaña_Alambrico(start_date, end_date)
    return f"Reporte Alambrico ejecutado correctamente de {start_date} al {end_date}"

def Alambrico_Kpi(end_date):
    KpiAlambrico(end_date,)
    return f"Reporte Alambrico ejecutado correctamente al {end_date}"

def Alambrico_Rd_Amg_App(start_date, end_date):
    Campaña_Alambrico_Rd_Amg_App(start_date, end_date)
    return f"Reporte Alambrico ejecutado correctamente de {start_date} al {end_date}"
####################################################################################################################################
##--> ALAMBRICO  
def Corporativo_report_Nomina(end_date):
    CargaNominaCorporativo(end_date,)
    return f"Reporte Corporativo ejecutado correctamente al {end_date}"

def Corporativo_report_1(start_date, end_date):
    Campaña_Corporativo(start_date, end_date)
    return f"Reporte Corporativo ejecutado correctamente de {start_date} al {end_date}"

def Corporativo_Kpi(end_date):
    KpiCorporativo(end_date,)
    return f"Reporte Corporativo ejecutado correctamente al {end_date}"


####################################################################################################################################
##--> Mesa de Ayuda  
def MesaAyuda_report_Nomina(end_date):
    CargaNominaMesaAyuda(end_date,)
    return f"Reporte Mesa de Ayuda ejecutado correctamente al {end_date}"

def MesaAyuda_report_1(start_date, end_date):
    Campaña_MesaAyuda(start_date, end_date)
    return f"Reporte Mesa de Ayuda ejecutado correctamente de {start_date} al {end_date}"

def MesaAyuda_Kpi(end_date):
    KpiMesaAyuda(end_date,)
    return f"Reporte Mesa de Ayuda ejecutado correctamente al {end_date}"


####################################################################################################################################
##--> Inalambrico 


def Inalambrico_report_1(start_date, end_date):
    Campaña_Inalambrico(start_date, end_date)
    return f"Reporte Inalambrico ejecutado correctamente de {start_date} al {end_date}"


####################################################################################################################################
##--> mULTISKILL 
def Activaciones_report_Nomina(end_date):
    CargaNominaActivaciones(end_date,)
    return f"Reporte Activaciones ejecutado correctamente al {end_date}"

def Activaciones_report_1(start_date, end_date):
    Campaña_Activaciones(start_date, end_date)
    return f"Reporte Activaciones ejecutado correctamente de {start_date} al {end_date}"

def Activaciones_Kpi(end_date):
    KpiActivaciones(end_date,)
    return f"Reporte Activaciones ejecutado correctamente al {end_date}"

def Activaciones_otros_Kpi(end_date):
    Campaña_Activaciones_otros(end_date,)
    return f"Reporte Activaciones ejecutado correctamente al {end_date}"


####################################################################################################################################
##--> Mesa Soporte 

def MesaSoporte_report_Nomina(end_date):
    CargaNominaMesaSoporte(end_date,)
    return f"Reporte Activaciones ejecutado correctamente al {end_date}"

def MesaSoporte_navicat_report(start_date,end_date):
    Campaña_MesaSoporte_Navicat(start_date,end_date)
    return f"Reporte Activaciones ejecutado correctamente al {end_date}"

def MesaSoporte_Interacciones_report(start_date,end_date):
    Interacciones_MesaSoporte(start_date,end_date)
    return f"Reporte Activaciones ejecutado correctamente al {end_date}"

def MesaSoporte_Kpi(end_date):
    KpiMesaSoporte(end_date,)
    return f"Reporte Activaciones ejecutado correctamente al {end_date}"

####################################################################################################################################
##--> SVFF
def SVFF_report_Nomina(end_date):
    CargaNominaSVFF(end_date,)
    return f"Reporte SVFF ejecutado correctamente al {end_date}"

##--> Seguimiento
def Seguimiento_report_Nomina(end_date):
    CargaNominaSeguimiento(end_date,)
    return f"Reporte Seguimiento ejecutado correctamente al {end_date}"