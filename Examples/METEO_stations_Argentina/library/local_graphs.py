
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from SMN_climatology_stations import get_data_processed, get_info_stn, get_list_variables

def get_colormap(xdim, ydim):
    """
    Generate a colormap for the (xdim, ydim) space.
    """
    norm = matplotlib.colors.Normalize(vmin=1, vmax=50)

    blue = np.zeros((ydim,xdim))
    red = np.zeros((ydim,xdim))
    green = np.zeros((ydim,xdim))

    for i in range(ydim):
        red[i,:] = np.linspace(0,1,xdim)
        blue[:,i] = np.linspace(0,1,xdim)
    green[:] = 1-(red+blue)/2.
    return red, blue, green

#######################################


# Cluster map with localization of stations
def clusters_element(xdim, ydim, mapvect, stations_name, outdir):

   red, blue, green = get_colormap(xdim, ydim)

   # nb of element plotted per localization
   a = np.zeros((ydim,xdim))

   # Get mapvect for last iteration
   mapv_final = mapvect

   plt.figure(figsize = (12,8))
 
   for i in range(xdim):
       for j in range(ydim):
           plt.plot(i+1,j+1, color = (red[j,i], green[j,i],blue[j,i], 1.0), marker = "o")

   for index_station in range(len(mapvect)):
       koho_vect_x,koho_vect_y = mapvect[index_station]
       a[koho_vect_y, koho_vect_x] += 1
       i = koho_vect_x; j = koho_vect_y
       plt.text(i+1,j+1+a[j, i]*0.2,stations_name[index_station], fontsize =5) 
    
   plt.xlim(0,xdim+2)
   plt.xticks(np.arange(1,xdim+1))
   plt.ylim(0,ydim+2)
   plt.yticks(np.arange(1,ydim+1))
   plt.savefig(outdir, dpi = 500)
   plt.close()
   
#######################################   
# Map with localization of stations and their cluster color
def cluster_map(xdim, ydim, mapvect, stations_name, outdir):
    red, blue, green = get_colormap(xdim, ydim)
    plt.figure()
    ax1 = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax1.add_feature(cartopy.feature.LAND)
    ax1.add_feature(cartopy.feature.OCEAN)
    ax1.add_feature(cartopy.feature.COASTLINE)
    ax1.add_feature(cartopy.feature.BORDERS)
    ax1.set_extent([-80,-50,-57,-20])
    
    for index_station in range(len(mapvect)):
        koho_vect_x,koho_vect_y = mapvect[index_station]  
    
        st = get_info_stn(stations_name[index_station])
        i = koho_vect_x; j = koho_vect_y
        plt.plot(st.lon, st.lat, marker = "o", color = (red[j,i], green[j,i],blue[j,i], 1.0))

    plt.savefig(outdir, dpi = 500)
    plt.close()
  

