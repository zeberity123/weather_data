import os
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import h5py
import shapefile as shp

clouds_data_dir = f'/media/ubuntu/LaCie/clouds_OMI_MINDS_NO2'
temperature_data_dir = f'/media/ubuntu/LaCie/temperature_M2I1NXASM'
precipitaion_data_dir = f'/media/ubuntu/LaCie/precipitation_3B-HHR'

# -- read an IMERG HDF5 file
precipitaion_file_list = os.listdir(precipitaion_data_dir)

filename = '3B-HHR.MS.MRG.3IMERG.20220101-S000000-E002959.0000.V07B.HDF5'
file = f'{precipitaion_data_dir}/{filename}'
data = h5py.File(file,'r')

# -- extract the 3600x1800 element precipitation array.
# For Version 6 IMERG HDF5 files, read the "precipitationCal"
# variable if it is a half-hour file and the "precipitation"
# variable if it is a monthly file.  For Version 7, the variable
# is "precipitation" for both durations.
precip = data['/Grid/precipitation'][:]

# -- get rid of the dummy single-element first dimension,
# transpose to get longitude on the x axis, and flip vertically
# so that latitude is displayed south to north as it should be
precip = np.flip( precip[0,:,:].transpose(), axis=0 )

# -- display the precipitation data. Regions with missing data
# values have negative values in the precip variable so allow
# the color table to extend to negative values.

plt.imshow( precip, vmin=-1, vmax=10, extent=[-180,180,-90,90] )

# -- add a color bar
cbar = plt.colorbar( )
cbar.set_label('millimeters/hour')

# -- display lat/lon grid lines
for lon in np.arange(-90,90+1,90):
  dummy = plt.plot( (lon,lon), (-90,+90), color="black", linewidth=1 )

for lat in np.arange(-60,60+1,30):
  dummy = plt.plot( (-180,+180), (lat,lat), color="black", linewidth=1 )

plt.savefig('precipitation_20220101.png', format='png', dpi=360)
plt.show()


