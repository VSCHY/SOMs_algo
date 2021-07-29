#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML_Climate : Pre Process ERA data

@author: Anthony Schrapffer
@institution: CIMA, UBA, Argentina
"""

###########################

# Library 

from netCDF4 import Dataset as NetCDFFile
from netCDF4 import num2date
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import sys
sys.path.append("/home/anthony/Documents/Doctorat/PROD/ML_Climate/2-Programs/")
from class_data_ERA import ERA_data as ERA 

###########################

class input_ML:
    def __init__(self, moistdir):
        self.moistconv = ERA(moistdir)
        self.moistconv.process_data()

    def process_input(self):
        s0 = self.moistconv.s[0]; s1 = self.moistconv.s[1]*self.moistconv.s[2]
        self.MLin = np.zeros((s0, s1)) 
        self.MLin[:,0:s1] = self.moistconv.data[:,:]
        self.map_dim = s1

###########################

