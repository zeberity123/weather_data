import os
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import cartopy.crs as ccrs

clouds_data_dir = f'/media/ubuntu/LaCie/clouds_OMI_MINDS_NO2'
temperature_data_dir = f'/media/ubuntu/LaCie/temperature_M2I1NXASM'
precipitaion_data_dir = f'/media/ubuntu/LaCie/precipitation_3B-HHR'

# -- read an IMERG HDF5 file
# clouds_file_list = os.listdir(clouds_data_dir)

filename = 'OMI-Aura_L2-OMI_MINDS_NO2_2022m0101t0237-o092892_v01-01-2022m0330t205144.nc'

sample_file = f'{clouds_data_dir}/{filename}'
# Read in NetCDF4 file (add a directory path if necessary):

data = Dataset(sample_file, mode='r')

# Run the following line below to print MERRA-2 metadata. This line will print attribute and variable information. From the 'variables(dimensions)' list, choose which variable(s) to read in below.
# print(data.groups['ANCILLARY_DATA'])

# Read in the 'T2M' 2-meter air temperature variable:
lons = data.groups['GEOLOCATION_DATA']['Longitude'][:]
lats = data.groups['GEOLOCATION_DATA']['Latitude'][:]
clouds = data.groups['ANCILLARY_DATA']['CloudPressure'][:]

# If using MERRA-2 data with multiple time indices in the file, the following line will extract only the first time index.
# Note: Changing T2M[0,:,:] to T2M[10,:,:] will subset to the 11th time index.

# T2M = T2M[:]

# Plot the data using matplotlib and cartopy

# Set the figure size, projection, and extent
fig = plt.figure(figsize=(8,4))
ax = plt.axes(projection=ccrs.Robinson())
ax.set_global()
ax.coastlines(resolution="110m",linewidth=1)
ax.gridlines(linestyle='--',color='black')

# Set contour levels, then draw the plot and a colorbar
clevs = np.arange(230,311,5)
plt.contourf(lons, lats, clouds, clevs, transform=ccrs.PlateCarree(),cmap=plt.cm.jet)
plt.title('OMI_MINDS_NO2_2022m0101t0237 CloudFraction', size=14)
cb = plt.colorbar(ax=ax, orientation="vertical", pad=0.02, aspect=16, shrink=0.8)
cb.set_label('K',size=12,rotation=0,labelpad=15)
cb.ax.tick_params(labelsize=10)

# Save the plot as a PNG image

fig.savefig('OMI_MINDS_NO2_2022m0101t0237.png', format='png', dpi=360)
fig.show()