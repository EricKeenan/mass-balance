'''
Usage:
conda activate alpine3d
python3 get_RF_ratio.py smet/-71.000_136.875.smet
'''

import numpy as np
import xarray as xr
import pandas as pd
import sys

import pyproj
from pyproj import Geod
from pyproj import Proj, transform
from fiona.crs import from_epsg
from osgeo import osr
from scipy import interpolate

# Function to convert lat/lon to epsg3031
def lat_lon_to_epsg3031(tgt_lat, tgt_lon):
    
    # Source and target EPSG
    src = osr.SpatialReference()
    tgt = osr.SpatialReference()
    src.ImportFromEPSG(4326) # WGS-84
    tgt.ImportFromEPSG(3031) # South Polar Stereo
    
    # Define transformation
    transform = osr.CoordinateTransformation(src, tgt)
    
    # Perform transformation
    coords = transform.TransformPoint(tgt_lat, tgt_lon)
    tgt_x, tgt_y = coords[0:2]
    
    return tgt_x, tgt_y

# Function to get ratio at lat/lon
def get_RF_M2_ratio(tgt_lat, tgt_lon):
    
    # Get M2 SMB at lat/lon
    M2_smb = xr.open_dataset("M2_annual-mean-SMB.nc")
    M2_smb = M2_smb['__xarray_dataarray_variable__']
    M2_smb = M2_smb.sel(lat=tgt_lat, lon=tgt_lon, method='nearest').values
    
    # Get RF at lat/lon
    tgt_x, tgt_y = lat_lon_to_epsg3031(tgt_lat, tgt_lon)
    M2_RF = xr.open_dataset("RF_Snow_Red_prelim.nc")
    M2_RF = M2_RF['IS2_opt'].sel(x=tgt_x, y=tgt_y, method='nearest').values
    
    # Get ratio
    RF_ratio = (M2_RF + M2_smb) / M2_smb
    
#     # Print info
#     print("Random Forest Ratio: " + str(RF_ratio))
#     print("MERRA-2 SMB [mm/yr]: " + str(M2_smb))
#     print("Random Forest Perturbation [mm/yr]: " + str(M2_RF))
    
    return RF_ratio, M2_smb, M2_RF

def read_smet_lat_lon(path):

    """ Reads a .smet file and returns a time series of the defined variable as a pandas data frame.
    Args:
        path (str): String pointing to the location of the .smet file to be read.
        var  (str): Variable you want to plot
    Returns:
        Time series of defined variable as a pandas data frame.
    """

    # Load .smet file as a Pandas data frame
    df = pd.read_csv(path)

    lat_row = np.where(df[df.columns[0]].str.startswith("latitude"))[0][0]
    lon_row = np.where(df[df.columns[0]].str.startswith("longitude"))[0][0]
    
    lat = float(df['SMET 1.1 ASCII'][lat_row].split()[-1])
    lon = float(df['SMET 1.1 ASCII'][lon_row].split()[-1])

    return lat, lon

# Get smet file path as command line argument
path = str(sys.argv[-1])
# print(path)

# Get lat/lon of smet file
lat, lon = read_smet_lat_lon(path)
# print(lat)
# print(lon)

# Print RF_ratio
RF_ratio, M2_smb, M2_RF = get_RF_M2_ratio(lat, lon)
if np.isnan(RF_ratio):
    RF_ratio = 1

# Add RF ratio to smet file
tgt_str = "units_multiplier = 1 1 1 1 1 1 1 " + str(RF_ratio) +  " 1\n"
# print(tgt_str)

with open(path, 'r') as f:
    in_file = f.readlines()
    
out_file = []
for line in in_file:
    out_file.append(line)  # copy each line, one by one
    if 'fields' in line:  # add a new entry, after a match
        out_file.append(tgt_str)

with open(path, 'w') as f:
    f.writelines(out_file)