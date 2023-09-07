import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd

def load_jxtn(filename):
    gdf = gpd.read_file(filename)
    return gdf

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

# Load jurisdiction
bolton = load_jxtn('Bolton.geojson')

# Calculate areas of all districts in jurisdiction
bolton_areas = get_areas(bolton)

# Calculate total area of jurisdiction by summing areas of base districts only,
# then converting square meters to square miles

totalarea = get_total_area(bolton_areas)
print('The total area in square miles of Bolton is: ' + str(totalarea))

# Calculate area of districts where single-family housing is allowable by right
singlefamily = np.sum(by_right('1-Family Treatment', bolton_areas)['area'])
print('The area of districts where single-family housing is allowable by right is: ', str(singlefamily))

print('Single-family by right represents ', str(round(100*singlefamily/totalarea, 2)), '% of the area in Bolton.')