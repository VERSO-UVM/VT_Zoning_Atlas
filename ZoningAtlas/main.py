## IMPORTS

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd

## FUNCTION DECLARATION

def consolidate_data(folder, gis_or_zoning): # gis_or_zoning is a string variable with value of either 'gis' or 'zoning'
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
    gdf = get_areas(gdf)
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

def due_process(housingtype, gdf, process_label):
    by_right = pd.DataFrame(gdf.loc[gdf[housingtype] == process_label], columns = gdf.columns)
    return by_right

## MAIN CODE RETURNING ANALYTICS REQUESTED BY NATIONAL ZONING ATLAS

# Load data for all districts in directory into a single GeoDataFrame
all_district_geodata = consolidate_data('districts', 'gis')
# all_district_zoning_data = consolidate_data('districts', 'zoning')

# Load data for all jurisdictions in directory into a single DataFrame
all_jxtn_data = consolidate_data('jxtns', 'zoning')

''' Jurisdiction characteristics '''

# Total number of jurisdictions analyzed
print('Total number of jurisdictions: ', len(all_jxtn_data))

# Side-by-side barplot of jurisdiction types both with and without zoning
govt_types = all_jxtn_data.groupby(['Type of Government', 'Does It Have Zoning?']).size().reset_index(name='count')
xlabels = []
heights = []
for index, row in govt_types.iterrows():
    if govt_types.loc[index]['Does It Have Zoning?'] == 'Yes':
        zoninglabel = ' With Zoning'
    elif govt_types.loc[index]['Does It Have Zoning?'] == 'No':
        zoninglabel = ' Without Zoning'
    xlabels.append(govt_types.loc[index]['Type of Government'] + zoninglabel)
    heights.append(govt_types.loc[index]['count'])

yticks = np.arange(min(heights)-1, max(heights)+1, max(heights)-min(heights))
plt.bar(xlabels, heights)
plt.xticks(rotation = 45)
plt.yticks(yticks)
plt.title('Types of Jurisdictional Government in Dataset')
plt.tight_layout()
plt.show()

# Number and percentage of jurisdictions with zoning
print('Number of jurisdictions with zoning: ', all_jxtn_data['Does It Have Zoning?'].value_counts()['Yes'])
print('Percentage of jurisdictions with zoning: ', all_jxtn_data['Does It Have Zoning?'].value_counts()['Yes']/len(all_jxtn_data))

# Total # pages of zoning text analyzed
# print(all_jxtn_data['# of Pages in the Zoning Code'])
# # all_jxtn_data['# of Pages in the Zoning Code'].astype(int, copy = False)
# print('Total number of pages of zoning text analyzed: ', np.sum(all_jxtn_data['# of Pages in the Zoning Code']))
#
# # Average # pages in each zoning text
# print('Average number of pages per zoning text: ', np.average(all_jxtn_data['# of Pages in the Zoning Code']))

# Calculate areas of all districts in jurisdiction
for jxtn in all_district_geodata['Jurisdiction'].unique():
    print('Total area zoned, including overlays, in ', jxtn, ': ', sum(all_district_geodata.loc[all_district_geodata['Jurisdiction'] == jxtn]['area']))

# Calculate total area of jurisdiction by summing areas of base districts only,
# then converting square meters to square miles
bolton_areas = all_district_geodata.loc[all_district_geodata['Jurisdiction'] == 'Bolton']
totalarea = get_total_area(bolton_areas)
print('The total area in square miles of Bolton (excluding overlays) is: ' + str(totalarea))

# Calculate area of districts where single-family housing is allowable by right
singlefamily = np.sum(due_process('1-Family Treatment', bolton_areas, 'Allowed/Conditional')['area'])
print('The area of districts where single-family housing is allowable by right is: ', str(singlefamily))

print('Single-family by right represents ', str(round(100*singlefamily/totalarea, 2)), '% of the area in Bolton.')