#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMN climatology stations : Pre Process stations

@author: Anthony Schrapffer
@institution: CIMA, UBA, Argentina
"""

###########################

# Library 

import sys
sys.path.append("/home/anthony/Documents/Doctorat/PROD/ML_Climate/2-Programs")
import pandas as pd
import numpy as np
from SMN_read_info_stations import get_stations_info

###########################

dire = "/home/anthony/Documents/Doctorat/PROD/ML_Climate/1-Originals/DATA_SMN/estadisticasTREATED.txt"

df = pd.read_csv(dire, sep="\t",encoding = "ISO-8859-1")

# Stations
STATIONS = np.unique(np.array(df["Estación"].values, dtype = np.str))

# Get list of variables
VARIABLES = np.array(df.values[:8,1], dtype=np.str)

# Get information about stations (other py)
ESTACIONES, ESTACIONES_NAME = get_stations_info()

###########################

# Functions 

# var_index : list with variables we wan to consider 
# ex: [0,1] = only 1st and 2nd variables

# Get informations

def get_list_variables(var_index = []):
    """
    Get list of reduced variables
    """
    L_var = VARIABLES[var_index]
    return L_var

def get_info_stn(stn):
    """
    Get information about the station (stn)
    """
    if stn == "AEROPARQUE AERO":
        stcheck = 'AEROPARQUE BUENOS AIRES AERO'
    elif stn == "LA QUIACA OBS.":
        stcheck = "LA QUIACA"
    elif stn == "SAUCE VIEJO AERO":
        stcheck = "SANTA FE AERO"
    else:
        stcheck = stn.replace("Í", "I").replace("Á", "A").replace("Ó", "O").replace("Ü", "U")
        stcheck = stcheck.replace("É", "E").replace("Ú", "U")
    index_st = np.where(ESTACIONES_NAME == stcheck)[0][0]
    
    return ESTACIONES[index_st]

# Read and convert data

def get_var_from_st(stn, var_index=[]):
    """
    Extract vector of datas for variables in var_index 
    for stations (stn)
    """    
    first = df.loc[df["Estación"] == stn] 
    try:
        v_out = np.array(first.loc[first["Valor Medio de"] == VARIABLES[var_index[0]]].values[0,2:], dtype = np.float)
    except:
        return None
    for vari in var_index[1:]:
        try:
            values = np.array(first.loc[first["Valor Medio de"] == VARIABLES[vari]].values[0,2:], dtype = np.float)
            v_out = np.hstack((v_out, values))
        except:
            return None
    return v_out

def get_data_processed(var_index):
    """
    Get data for all the stations without missing data
    """
    stations_data = []
    stations_name = []
    
    for st in STATIONS:
        data_from_st = get_var_from_st(st, var_index)
        if data_from_st is not None:
            stations_data.append(data_from_st)        
            stations_name.append(st)
    
    stations_data = np.array(stations_data)
    return stations_name, stations_data

# Post process 

def vect2station_data(vect, var_index):
    """
    Convert data from vector (nb_var*12) to variable vs month (nb_var, 12)
    """
    station_data = np.reshape(vect, (len(var_index), 12))
    return station_data     

###################################

if __name__ == "__main__":
    # Test
    work_var_index = [0,1,2,3,5,6,7]
    work_var = get_list_variables(work_var_index)
    stations_name, stations_data = get_data_processed(work_var_index)
    
    # Test retrouver informations stations
    print(VARIABLES)
    print(len(ESTACIONES))

    
