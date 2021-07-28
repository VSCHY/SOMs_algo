#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMN climatology stations : informations about stations
w/ a little help from : https://github.com/fmartin92/smn-api

@author: Anthony Schrapffer
@institution: CIMA, UBA, Argentina
"""

###########################

# Library 

import pandas as pd
import numpy as np
import unidecode
import copy

###################################

# Class Estacion to group information from stations

class Estacion:
    def __init__(self, params):
        (self.nombre, self.provincia, self.oaci, self.latitud_gr,
         self.latitud_min, self.longitud_gr, self.longitud_min,
         self.altura, self.numero) = params
         
        self.lon = self.longitud_gr+np.sign(self.longitud_gr)*self.longitud_min/60.
        self.lat = self.latitud_gr+np.sign(self.latitud_gr)*self.latitud_min/60.
         
    def show(self):
        print(self.nombre, self.provincia, self.oaci, self.latitud_gr, \
              self.latitud_min, self.longitud_gr, self.longitud_min, \
              self.altura, self.numero)

# Direction of file 
dire = "/home/anthony/Documents/Doctorat/PROD/ML_Climate/1-Originals/DATA_SMN/estaciones_smn.txt"

with open(dire) as f:
    datos_estaciones = f.read().split('\n')[:-1]

estaciones = []

for estacion in datos_estaciones:
    nombre = estacion[:31].rstrip()
    provincia = estacion[31:68].rstrip()
    resto_de_datos = estacion[67:].split()
    oaci = resto_de_datos.pop()
    datos_numericos = [int(dato) for dato in resto_de_datos]
    estaciones.append(Estacion([nombre, provincia, oaci] + datos_numericos))

###################################

# Function

def get_stations_info():    
    """
    Obtener informaciones para las estaciones
    estaciones : list of element of type Estacion
    estaciones_name : array 1D of stations name to navigate quicker
    """
    estaciones_name = np.array([st.nombre for st in estaciones])
    return estaciones, estaciones_name 
