#!/usr/bin/env python3
"""
SOMs of SMN meteorological stations
"""
import sys
sys.path.append("../../")
sys.path.append("./library")
import numpy as np
import numpy.ma as ma

# Global function
from SOMS import WTU
from lib_graphs import kohonen_map

# Local class
from SMN_climatology_stations import get_data_processed, get_info_stn, get_list_variables

# Local lib
from local_graphs import cluster_map, clusters_element

##################################

# Pre-process

work_var_index = [0,1,2,3,6,7]
work_var = get_list_variables(work_var_index)

stations_name, stations_data = get_data_processed(work_var_index)

###############################

# SOMs calculation

# Parameters

n_iter = 200
xdim = 5
ydim = 5
map_dim = len(stations_data[0,:])

# SOM initilization and training
som = WTU(xdim, ydim, map_dim, n_iter)
som.fit(stations_data)

# Get the cluster
out = som.get_centroids()

##########################
#
# Prepare analysis

# mapvect : cluster for each element
mapvect = som.map_vects(stations_data)

number_elements_Koho = np.zeros((ydim,xdim))
# Nb of elements by cluster
for koho_vect_x,koho_vect_y in mapvect:
    number_elements_Koho[koho_vect_y,koho_vect_x] +=1

##########################

# Kohonen map with number of element by cluster
kohonen_map(xdim, ydim, data = number_elements_Koho, outdir = "./Graphics/Kohonen_map.png")

# Cluster map with localization of stations
clusters_element(xdim, ydim, mapvect, stations_name, "./Graphics/clusters_element.png")

# Map with localization of stations and their cluster color
cluster_map(xdim, ydim, mapvect, stations_name, "./Graphics/cluster_map.png")



