#!/usr/bin/env python3
"""

"""
import sys
sys.path.append("./library")
sys.path.append("../../")


from netCDF4 import Dataset as NetCDFFile
import numpy as np
import numpy.ma as ma
from class_data_ER5moist import input_ML
#
from SOMS import WTU
from netcdf_output import output_SOM_NetCDF_moistconv
#
import matplotlib.pyplot as plt

##################################
#
# Pre-process
moistdir = "./Originals/PANTANAL_vimd_single-level_JFD_1980-2010_daily.nc"

mlin = input_ML(moistdir)
mlin.process_input()

################################
#
# SOMs calculation

# Parameters

n_iter = 150
xdim = 5 # m
ydim = 5 # n
map_dim = mlin.map_dim

# SOM initilization and training
som = WTU(xdim, ydim, map_dim, n_iter)
som.fit(mlin.moistconv.data)

# Get the cluster
out = som.get_centroids()

##########################
## Preparation for output

# Create output array
shape_lonlat = mlin.moistconv.shape_lonlat

moistconv = np.zeros((ydim,xdim,shape_lonlat[0],shape_lonlat[1]))

# Fullfill output array

for n in range(ydim):
    for m in range(xdim):
        data_md = mlin.moistconv.convert_vect2array(out[m][n])
        moistconv[n,m,:,:] = data_md

mapvect = som.map_vects(mlin.moistconv.data)

# Save Output
output_ncdir = "./output.nc"
output_SOM_NetCDF_moistconv(output_ncdir, mlin, xdim, ydim, moistconv, mapvect)

##########################
#        
# Output
"""
# Get number of event

Koho = np.zeros((ydim,xdim))

for koho_vect_x,koho_vect_y in mapvect_last_iter:
    Koho[koho_vect_y,koho_vect_x] +=1
    
def distance_iter(iteration):
    out = som.get_centroids()[iteration]
    l = 0
    i = 0
    for koho_vect_x,koho_vect_y in mapvect[iteration]:
        l+= LA.norm(mlin.data[i,:]-out[koho_vect_x][koho_vect_y])/map_dim
        i+=1
    return l

L = [distance_iter(i) for i in range(n_iter)]


##########################
# Graphics

# Plot distance 
plt.figure()
plt.plot(np.arange(n_iter), L)
plt.xlabel("n iteration")
plt.ylabel("$\sum_{days} |vect(d)-cluster(d)|$")
plt.title("Evolution of distance")
plt.savefig("./evolution.png")

# Plot Kohonen map
plt.figure()

plt.pcolormesh(np.flip(Koho[:,:], axis = 0))

plt.xlabel("m")
plt.xlim((0,xdim))
plt.ylim((0,ydim))
plt.xticks(np.arange(0.5,xdim), np.arange(1,xdim+1))
plt.yticks(np.arange(0.5,ydim), np.flip(np.arange(1,ydim+1)))

plt.ylabel("n")
plt.colorbar()
plt.title("kohonen Map")
plt.savefig("./Kohonen_map.png")
"""

