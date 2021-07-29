#!/usr/bin/env python3
import sys
#sys.path.append("/home/anthony/Documents/Doctorat/PROD/ML_Climate/2-Programs")
sys.path.append("/home/anthony/Documents/Doctorat/PROD/ML_Climate/3-Test/7-Moist_Pantanal/Programs")
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from netCDF4 import Dataset as NetCDFFile
from netCDF4 import num2date
import numpy as np
import numpy.ma as ma
import matplotlib
import matplotlib.gridspec as gridspec
import pandas as pd
import cartopy.io.shapereader as shpreader


from class_data_ER5moist import input_ML
from netcdf_output import output_SOM_NetCDF_moistconv
from numpy import linalg as LA

##########################

moistdir = "./Originals/PANTANAL_vimd_single-level_JFD_1980-2010_daily.nc"
dout = "./output.nc"

dgraphs = "./Graphics/"

##########################

class output:
    def __init__(self, output):
        self.nc = NetCDFFile(output, "r")
        self.lon = self.nc.variables["lon"][:]
        self.lat = self.nc.variables["lat"][:]
        time = self.nc.variables["time"]
        self.dtime = num2date(time[:], time.units)
        self.xdim = len(self.nc.variables["m"][:])
        self.ydim = len(self.nc.variables["n"][:])
        self.ndim = self.ydim ; self.mdim = self.xdim
        
        self.ml = np.arange(0.5,6.5)
    
        self.moistconv_cluster = self.nc.variables["moistconv"][:] # n,m,lat, lon
        self.mapvect_m = self.nc.variables["mapvect_m"][:] # time
        self.mapvect_n = self.nc.variables["mapvect_n"][:] # time
        
    def koho_map(self):
        Koho = np.zeros((self.ydim,self.xdim))
        
        for koho_vect_x,koho_vect_y in zip(self.mapvect_m, self.mapvect_n):
            Koho[int(koho_vect_y),int(koho_vect_x)] +=1
        # y = n = vertical 
        self.Koho = Koho
        
    def koho_filter(self, filter):
        Koho = np.zeros((self.ydim,self.xdim))
        
        for fil, koho_vect_x,koho_vect_y in zip(filter, self.mapvect_m, self.mapvect_n):
            if fil==1:
                Koho[int(koho_vect_y),int(koho_vect_x)] +=1
        # y = n = vertical 
        return Koho
    
    def plot_koho(self, koho, title, namefig):
        plt.figure(figsize= (6,5))    
        plt.pcolor(self.ml, self.ml, np.flip(koho, axis = 0))
        plt.xticks(np.arange(1,6))
        plt.yticks(np.arange(1,6), np.flip(np.arange(1,6)))
        plt.colorbar()
        plt.title(title)
        plt.savefig(dgraphs + namefig)
        plt.close()
        

##########################      
            
moistconv = input_ML(moistdir).moistconv.data
clu = output(dout)
clu.koho_map()

##########################

# Plot distribution cluster
clu.plot_koho(clu.Koho, "Distribution Kohonen map", "1-Distribution_Kohonen_map.png")

##########################
 
def plot_map(gs, col, row, data, title):
    plt.subplot(gs[row, col], projection=ccrs.PlateCarree())
    ax = plt.gca()
    ax.add_feature(cartopy.feature.BORDERS)
    ax.add_feature(cartopy.feature.COASTLINE)
    cbar = ax.contourf(clu.lon, clu.lat, data, levels = np.arange(-3,2.25,0.25), vmin = -1.5, vmax = 1.)
    ax.ylabel = str(col+1)
    #plt.title(title)
    plt.colorbar(cbar)
    #return cbar

fig = plt.figure(figsize= (10,10))    
gs = matplotlib.gridspec.GridSpec(5, 5)
for n in range(0,5):
    for m in range(0,5):
        plot_map(gs, m, n, clu.moistconv_cluster[n,m,:,:], "n = {0} / m = {1}".format(n+1,m+1))
        
        ax = plt.gca()
        if m ==0:
            ax.text(-0.2, 0.5, n+1, va='bottom', ha='center',
                    rotation='horizontal', rotation_mode='anchor',
                    transform=ax.transAxes, fontsize = 20)
            if n ==2: 
                 ax.text(-0.5, 0.5, "n", va='bottom', ha='center',
                         rotation='horizontal', rotation_mode='anchor',
                         transform=ax.transAxes, fontsize = 30)                
        if n == 0:
             ax.text(0.5, 1.1, m+1, va='bottom', ha='center',
                    rotation='horizontal', rotation_mode='anchor',
                    transform=ax.transAxes, fontsize = 20)
             if m ==2:
                 ax.text(0.5, 1.3, "m", va='bottom', ha='center',
                         rotation='horizontal', rotation_mode='anchor',
                         transform=ax.transAxes, fontsize = 30)

plt.savefig(dgraphs + "2-Clusters.png")
plt.close()

#Vertically integrated moisture divergence
# + grand = + divergent -> - bonne condition precipitation
# + grand en valeur absolu -> + d'humidit2 en jeu


##########################
#
"""
Levy, M. C. (2017). 
Rain gauge data for the Brazilian rainforest-savanna transition zone, 
HydroShare, http://www.hydroshare.org/resource/9ee10ae69e074f819f023df73e15c4e1
"""

# Prepare rainfall dataset
rain_data = "./Originals/rain_data.csv"
dfrain = pd.read_csv(rain_data)
SUM = (dfrain['month'] == 12) | (dfrain['month'] == 1) | (dfrain['month'] == 2)
dfrain = dfrain[SUM]
YEAR = (dfrain['year'] >= 1980) & (dfrain['year'] < 2011)
dfrain = dfrain[YEAR]

#site = np.unique(dfrain['site'].to_numpy())

##########

D= {}
D[2157004] = ["Porto Murtinho",-21.7014,-57.8917]
D[1556004] = ["Cuiabá", -15.6333, -56.1]
D[1756001] = ["SÃO JOSÉ DO PIQUIRI",-17.2914 , -56.3847]
D[1755003] = ["SÃO JERÔNIMO", -17.2017, -56.0086]
D[1656003] = ["SÃO JOSÉ DO BORIRÉU", -16.9211, -56.2236]
D[1657003] = ["CÁCERES"	, -16.0817, -57.6942]
D[1654000] = ["RONDONÓPOLIS", -16.4711, -54.6561]
D[1455002] = ["COIMBRA - PORTO DE CIMA", -14.8833, -55.8667]
D[1957002] = ["CORUMBÁ (ETA)", -19.0058, -57.6019]
D[1957006] = ["PORTO ESPERANÇA",-19.6008, -57.4381]
D[1957004] = ["FORTE COIMBRA", -19.9186, -57.7894]
D[1957003] = ["PORTO DA MANGA", -19.2583, -57.2353]
D[1756003] = ["PORTO DO ALEGRE", -17.6233, -56.965]
D[1854005] = ["COXIM", -18.5, -54.9333]
D[2056001] = ["MIRANDA", -20.2408, -56.3958]
#D[] = ""

# Intégrer plus de statins et les regrouper par zone
# Prendre les regionss cf hydroBasins Thienan puis voir si pt contenu dans zone

def plot_locst(ncol, nrow, ind, stnum):
    ax = plt.subplot(ncol, nrow, ind, projection=ccrs.PlateCarree())
    ax.set_extent([-62,-52,-23,-14])

    # BORDERS
    ax.add_feature(cartopy.feature.BORDERS)
    """
    geo_reg_shp = shpreader.natural_earth(resolution='50m', category='cultural',
                            name='admin-0-boundary-lines')
    geo_reg = shpreader.Reader(geo_reg_shp)
    geo_reg = geo_reg.records()
    for rec in geo_reg:
        ax.add_geometries( [rec.geometry], ccrs.PlateCarree(), edgecolor="r", facecolor='none')#, linewidth = self.pantlw )
    """
    # PANTANAL & UPRB
    geo_reg_shp = shpreader.natural_earth(resolution='50m', category='physical',
                            name='geography_regions_polys')
    geo_reg = shpreader.Reader(geo_reg_shp)
    geo_reg = geo_reg.records()
    #
    # shapefile of the UPRB
    UPRB_shp = "/home/anthony/Documents/Doctorat/Tools/[DATA] HydroBASINS/UPRB.shp"
    UPRB = shpreader.Reader(UPRB_shp)
    UPRB = UPRB.records()
    #
    for rec in geo_reg:
        if (rec.attributes["name_es"]=="Pantanal"):
            ax.add_geometries( [rec.geometry], ccrs.PlateCarree(), edgecolor="r", facecolor='none')#, linewidth = self.pantlw )
    #
    for rec in UPRB:
        ax.add_geometries( [rec.geometry], ccrs.PlateCarree(), edgecolor="b", facecolor='none')#, linewidth = self.pantlw )
    # 
    for n in stnum:
        L = D[n]
        plt.plot(L[2],L[1], color = "b", marker = "o")

def plot_koho(ncol, nrow, ind, koho, title, namefig):
    plt.subplot(ncol, nrow, ind)    
    plt.pcolor(clu.ml, clu.ml, np.flip(koho, axis = 0))
    plt.xticks(np.arange(1,6))
    plt.yticks(np.arange(1,6), np.flip(np.arange(1,6)))
    plt.colorbar()
    plt.title(title)



stnum = list(D.keys())
plot_locst(1, 1, 1, stnum) 
plt.savefig(dgraphs + "stations.png")
plt.close()



# Contour UPRB (smoothed) et contour Pantanal

for index, L in D.items():
    PM =  dfrain['site']== index
    dfrain_PM = dfrain[PM]

    filtre = (dfrain_PM["value"] > 2).to_numpy()
    rainy = np.full(filtre.shape, 1)
    rainy[filtre == False] = 0

    koho_PM = clu.koho_filter(rainy)
    
    plt.figure(figsize= (10,5))
    plot_koho(1, 2, 2, koho_PM, "PM daily rainfall > 5mm", "3-"+L[0]+"_PRECIP.png")
    plot_locst(1, 2, 1, [index])
    plt.savefig(dgraphs + "3-"+L[0]+"_PRECIP.png")
    plt.close()

