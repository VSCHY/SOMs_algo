#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
netcdf_output : Save the cluster to NetCDF

@author: Anthony Schrapffer
@institution: CIMA, UBA, Argentina
"""

###########################

# Library 

from netCDF4 import Dataset as NetCDFFile
from netCDF4 import date2num
import numpy as np

###########################

# Save output SOM from wind study to NetCDF
#     will have the clusters
# For analysis : will need a function to get the emplacement of each day

def output_SOM_NetCDF_moistconv(output_ncdir, mlin, m_size, n_size, moistconv_in, mapvect_last_iter):
    with NetCDFFile(output_ncdir, "w") as foo:
        lats = mlin.moistconv.lat[:]
        lons = mlin.moistconv.lon[:]
        tlen = len(mlin.moistconv.time)

        # Create Dimensions
        m = foo.createDimension('m', m_size)
        n = foo.createDimension('n', n_size)    
        lat = foo.createDimension('lat', lats.shape[0])
        lon = foo.createDimension('lon', lons.shape[0])
        time = foo.createDimension('time', tlen)
 
        # Create Dimensions variables
        vlon = foo.createVariable('lon', np.float32,('lon'))
        vlat = foo.createVariable('lat', np.float32,('lat'))    
        vm = foo.createVariable('m', np.int,('m'))
        vn = foo.createVariable('n', np.int,('n'))
        vtime = foo.createVariable('time', np.int,('time'))

        # Fulfill Dimensions variables and their units
        vlat[:] = lats[:]
        vlon[:] = lons[:]
        vm[:] = np.arange(1,m_size+1)
        vn[:] = np.arange(1,n_size+1)
        # Units
        vlat.units = mlin.moistconv.lat.units
        vlon.units = mlin.moistconv.lon.units
        vtime[:] = mlin.moistconv.time
        vtime.units = mlin.moistconv.time_units
        
        # Moistconv from clusters
        moistconv = foo.createVariable('moistconv', np.float32,('n', 'm','lat','lon'))    
        moistconv[:] = moistconv_in[:]
        
        # Mapvect
        mapvect_var_m = foo.createVariable('mapvect_m', np.float32,('time'))
        mapvect_var_n = foo.createVariable('mapvect_n', np.float32,('time'))   
        
        for l in range(tlen):
            mapvect_var_m[l] = mapvect_last_iter[l][0]
            mapvect_var_n[l] = mapvect_last_iter[l][1]
        foo.sync()

def output_SOM_NetCDF(output_ncdir, mlin, m_size, n_size, precip, stage, mapvect):
    with NetCDFFile(output_ncdir, "w") as foo:
        
        # nc est le fichier UDEL -> avoir lat, lon

        lats = mlin.ud.lat
        lons = mlin.ud.lon
        y1 = mlin.ud.y1
        y2 = mlin.ud.y2
        nstat = mlin.riv.num_st

        # Create Dimensions
        m = foo.createDimension('m', m_size)
        n = foo.createDimension('n', n_size)    
        lat = foo.createDimension('lat', lats.shape[0])
        lon = foo.createDimension('lon', lons.shape[0])
        year = foo.createDimension('year', y2-y1+1)
        stat = foo.createDimension('station', nstat)
 
        # Create variables defining dimensions
        lon = foo.createVariable('lon', np.float32,('lon'))
        lat = foo.createVariable('lat', np.float32,('lat'))    
        m = foo.createVariable('m', np.int,('m'))
        n = foo.createVariable('n', np.int,('n'))
        year = foo.createVariable('year', np.int,('year'))
        stat = foo.createVariable('station', np.int,('station'))       

        # Fulfill
        lat[:] = lats[:]
        lon[:] = lons[:]
        m = np.arange(1,m_size+1)
        n = np.arange(1,n_size+1)
        # Units
        lat.units = lats.units
        lon.units = lons.units

        year[:] = np.arange(y1,y2+1)
        stat[:] = np.arange(nstat)
    
        # Variables
        pr = foo.createVariable('precip', np.float32,('n', 'm','lat','lon'))    
        riverstage = foo.createVariable('river', np.float32,('n', 'm','station'))
        mapvect_var_m = foo.createVariable('mapvect_m', np.float32,('year'))
        mapvect_var_n = foo.createVariable('mapvect_n', np.float32,('year'))

        # attributes
        pr.units = "mm/d"
        riverstage.units = "m"

        # Values    
        pr[:] = precip[:]
        riverstage[:] = stage[:]

        for l in range(y2-y1+1):
            mapvect_var_m[l] = mapvect[l][0]
            mapvect_var_n[l] = mapvect[l][1]
        foo.sync()


def output_SOM_NetCDF_basin(output_ncdir, m_size, n_size, output, mapvect, y0, y1):
    with NetCDFFile(output_ncdir, "w") as foo:

        # Create Dimensions
        m = foo.createDimension('m', m_size)
        n = foo.createDimension('n', n_size)    
        year = foo.createDimension('year', y1-y0+1)
        var = foo.createDimension('var', 4)
        month = foo.createDimension('months', 12)
 
        # Create variables defining dimensions
        v_month = foo.createVariable('months', np.float32,('months'))
        v_var = foo.createVariable('var', np.float32,('var'))
        v_year = foo.createVariable('year', np.float32,('year'))
        v_m = foo.createVariable('m', np.int,('m'))
        v_n = foo.createVariable('n', np.int,('n'))
        
        v_month[:] = np.arange(1,13)
        v_year = np.arange(y0,y1+1)
        v_var[:] = np.arange(1,5)
        v_m[:] = np.arange(1, m_size+1)
        v_n[:] = np.arange(1, n_size+1)


        # Variables
        out = foo.createVariable('cluster', np.float32,('n', 'm','var', 'months'))    

        mapvect_var_m = foo.createVariable('mapvect_m', np.float32,('year'))
        mapvect_var_n = foo.createVariable('mapvect_n', np.float32,('year'))

        # Values    
        out[:] = output[:]

        for l in range(len(v_year)):
            # map vect is x, y (m, n) our var i n, m
            mapvect_var_m[l] = mapvect[l][0]
            mapvect_var_n[l] = mapvect[l][1]

        foo.sync()
