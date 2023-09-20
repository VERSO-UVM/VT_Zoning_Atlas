import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd

def consolidate_districts(folder, gis_or_zoning): # gis_or_zoning is a string variable with value of either 'gis' or 'zoning'
    counter = 0
    base_dir = os.path.join(os.getcwd(), folder)
    for gjson in os.listdir(base_dir):
        thisfile = gjson
        f = os.path.join(base_dir, thisfile)
        with open(f, 'r') as filename:
            if gis_or_zoning == 'gis':
                this_jxtn = load_gis(f)
            else:
                if gis_or_zoning == 'zoning':
                    this_jxtn = load_zoning(filename)
                else:
                    print('Need to specify type of dataframe')
                    return(-1)
            if counter == 0:
                all_VT_zoning = this_jxtn
                counter = 1
            else:
                all_VT_zoning = pd.concat([this_jxtn, all_VT_zoning])
    return all_VT_zoning

def load_gis(filename):
    gdf = gpd.read_file(filename)
    return gdf

def load_zoning(filename): # can be used to load .csv of either jurisdiction or district data
    df = pd.read_csv(filename)
    return df

def get_areas(gdf):
    gdf_copy = gdf.copy()
    gdf_copy = gdf_copy.to_crs('epsg:3857')
    gdf_copy['area'] = gdf_copy.geometry.area
    gdf_copy['area'] = gdf_copy['area']*3.86102*10**(-7)
    return gdf_copy

def get_total_area(gdf):
    base_districts = gdf.loc[gdf['Overlay'] == 'No']
    return(sum(base_districts['area']))

def by_right(housingtype, gdf):
    by_right = pd.DataFrame(gdf.loc[gdf[housingtype] == "Allowed/Conditional"], columns = gdf.columns)
    return by_right

# Load data for all jurisdictions in directory into a single GeoDataFrame
all_VT_data = consolidate_districts('data', 'gis')

''' Jurisdiction characteristics '''

# Total number of jurisdictions analyzed
print('Total number of jurisdictions: ', len(all_VT_data['Jurisdiction'].unique()))

# Number and percentage of jurisdictions with zoning
print('Number of jurisdictions with zoning: ', all_VT_data['Zoning'].values_counts()['Yes'])

# Calculate areas of all districts in jurisdiction
# bolton_areas = get_areas(bolton)
#
# # Calculate total area of jurisdiction by summing areas of base districts only,
# # then converting square meters to square miles
#
# totalarea = get_total_area(bolton_areas)
# print('The total area in square miles of Bolton is: ' + str(totalarea))
#
# # Calculate area of districts where single-family housing is allowable by right
# singlefamily = np.sum(by_right('1-Family Treatment', bolton_areas)['area'])
# print('The area of districts where single-family housing is allowable by right is: ', str(singlefamily))
#
# print('Single-family by right represents ', str(round(100*singlefamily/totalarea, 2)), '% of the area in Bolton.')